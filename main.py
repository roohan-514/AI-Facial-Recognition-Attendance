import sys
import logging

import config
from src.face_recognition_system import FaceRecognitionSystem
from src.attendance_manager import AttendanceManager

logging.basicConfig(
    level=logging.INFO,
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_DIR / "system.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def run_attendance_system(frs: FaceRecognitionSystem, manager: AttendanceManager):
    import cv2

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

    if not cap.isOpened():
        logger.error("Cannot open camera")
        return

    frame_count = 0
    logger.info("Attendance system started. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_count += 1
        if frame_count % config.FRAME_SKIP != 0:
            cv2.imshow("AI Facial Recognition Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        results = frs.recognize_faces(frame)
        frame = frs.draw_results(frame, results)

        for res in results:
            if res["name"] != "Unknown":
                manager.mark_attendance(res["name"], res["confidence"])

        cv2.imshow("AI Facial Recognition Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("Attendance system stopped.")


def main():
    frs = FaceRecognitionSystem()
    manager = AttendanceManager()

    while True:
        print("\n" + "=" * 50)
        print("  AI FACIAL RECOGNITION ATTENDANCE SYSTEM")
        print("=" * 50)
        print("  1. Register a new face")
        print("  2. Start attendance system (real-time)")
        print("  3. Export attendance report (CSV)")
        print("  4. View attendance summary")
        print("  5. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            name = input("Enter person's name: ").strip()
            if name:
                if frs.register_face(name):
                    print(f"Face registered successfully for '{name}'")
                else:
                    print("Face registration failed.")
            else:
                print("Name cannot be empty.")

        elif choice == "2":
            run_attendance_system(frs, manager)

        elif choice == "3":
            path = manager.generate_report()
            print(f"Report exported to: {path}")

        elif choice == "4":
            date = input("Enter date (YYYY-MM-DD) or press Enter for all: ").strip()
            date = date if date else None
            summary = manager.get_summary(date)
            print(f"\nAttendance Summary for {summary['date']}:")
            print(f"  Total records: {summary['total']}")
            print(f"  Present:       {summary['present']}")
            print(f"  Unknown:       {summary['unknown']}")

        elif choice == "5":
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
