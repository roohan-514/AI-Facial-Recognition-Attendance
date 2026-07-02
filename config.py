import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
KNOWN_FACES_DIR = DATA_DIR / "known_faces"
ATTENDANCE_DB = DATA_DIR / "attendance.db"
REPORTS_DIR = DATA_DIR / "reports"
LOG_DIR = DATA_DIR / "logs"

for d in [DATA_DIR, KNOWN_FACES_DIR, REPORTS_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

RECOGNITION_THRESHOLD = 0.5
CONFIDENCE_THRESHOLD = 0.6

FRAME_SKIP = 2
COOLDOWN_MINUTES = 60

ATTENDANCE_TABLE = """
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    confidence REAL,
    UNIQUE(name, date)
)
"""

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

ENCODING_CACHE_FILE = DATA_DIR / "encodings_cache.pkl"
