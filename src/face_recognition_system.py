import cv2
import numpy as np
import pickle
import logging
import time
from pathlib import Path

import face_recognition

import config

logger = logging.getLogger(__name__)


class FaceRecognitionSystem:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.encoding_cache = config.ENCODING_CACHE_FILE
        self._load_known_faces()

    def _load_known_faces(self):
        if self.encoding_cache.exists():
            try:
                with open(self.encoding_cache, "rb") as f:
                    data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_names = data["names"]
                logger.info(
                    "Loaded %d known faces from cache", len(self.known_names)
                )
                return
            except (pickle.UnpicklingError, EOFError, KeyError) as e:
                logger.warning("Cache corrupt, rebuilding: %s", e)

        image_extensions = {".jpg", ".jpeg", ".png"}
        for img_path in config.KNOWN_FACES_DIR.iterdir():
            if img_path.suffix.lower() not in image_extensions:
                continue
            name = img_path.stem
            image = face_recognition.load_image_file(str(img_path))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_encodings.append(encodings[0])
                self.known_names.append(name)
                logger.debug("Registered face: %s", name)
            else:
                logger.warning("No face found in %s", img_path.name)

        self._save_cache()
        logger.info("Loaded %d known faces from disk", len(self.known_names))

    def _save_cache(self):
        data = {"encodings": self.known_encodings, "names": self.known_names}
        with open(self.encoding_cache, "wb") as f:
            pickle.dump(data, f)

    def register_face(self, name: str) -> bool:
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

        if not cap.isOpened():
            logger.error("Cannot open camera")
            return False

        face_images = []
        collected = 0
        required = 3

        logger.info("Look at the camera. Capturing %d samples...", required)

        while collected < required:
            ret, frame = cap.read()
            if not ret:
                continue

            small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)

            for top, right, bottom, left in boxes:
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            if boxes:
                face_images.append(frame.copy())
                collected += 1
                logger.info("Captured %d/%d", collected, required)
                time.sleep(0.5)

            cv2.imshow("Register Face - Press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        if collected < required:
            logger.error("Not enough samples captured")
            return False

        for i, img in enumerate(face_images):
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            if encodings:
                self.known_encodings.append(encodings[0])
                self.known_names.append(name)
                save_path = config.KNOWN_FACES_DIR / f"{name}_{i}.jpg"
                cv2.imwrite(str(save_path), img)
                logger.info("Saved %s", save_path.name)

        self._save_cache()
        logger.info("Face registered successfully for '%s'", name)
        return True

    def recognize_faces(self, frame: np.ndarray):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small = cv2.resize(rgb, (0, 0), fx=0.5, fy=0.5)
        boxes = face_recognition.face_locations(small)
        encodings = face_recognition.face_encodings(small, boxes)

        results = []
        for box, encoding in zip(boxes, encodings):
            top, right, bottom, left = [v * 2 for v in box]
            if self.known_encodings:
                distances = face_recognition.face_distance(
                    self.known_encodings, encoding
                )
                min_idx = np.argmin(distances)
                min_dist = distances[min_idx]

                if min_dist < config.RECOGNITION_THRESHOLD:
                    name = self.known_names[min_idx]
                    confidence = 1.0 - min_dist
                else:
                    name = "Unknown"
                    confidence = 0.0
            else:
                name = "Unknown"
                confidence = 0.0

            results.append({
                "name": name,
                "confidence": round(confidence, 3),
                "box": (top, right, bottom, left),
            })

        return results

    def draw_results(self, frame: np.ndarray, results: list):
        for res in results:
            top, right, bottom, left = res["box"]
            name = res["name"]
            confidence = res["confidence"]
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            label = f"{name} ({confidence:.2f})"
            cv2.putText(
                frame, label, (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2,
            )
        return frame
