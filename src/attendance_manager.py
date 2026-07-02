import sqlite3
import csv
import logging
from datetime import datetime
from pathlib import Path

import config

logger = logging.getLogger(__name__)


class AttendanceManager:
    def __init__(self):
        self.db_path = config.ATTENDANCE_DB
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute(config.ATTENDANCE_TABLE)
        conn.commit()
        conn.close()

    def mark_attendance(self, name: str, confidence: float = 0.0) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")

        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT time FROM attendance WHERE name = ? AND date = ?",
                (name, today),
            )
            existing = cursor.fetchone()

            if existing:
                logger.info(
                    "Attendance already marked for '%s' today at %s",
                    name, existing[0],
                )
                return False

            cursor.execute(
                "INSERT INTO attendance (name, date, time, confidence) "
                "VALUES (?, ?, ?, ?)",
                (name, today, now, confidence),
            )
            conn.commit()
            logger.info("Attendance marked for '%s' at %s", name, now)
            return True
        except sqlite3.IntegrityError:
            logger.warning("Duplicate attendance for '%s' today", name)
            return False
        finally:
            conn.close()

    def get_attendance(self, date: str | None = None) -> list[dict]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        if date:
            cursor.execute(
                "SELECT name, date, time, confidence FROM attendance "
                "WHERE date = ? ORDER BY time",
                (date,),
            )
        else:
            cursor.execute(
                "SELECT name, date, time, confidence FROM attendance "
                "ORDER BY date DESC, time"
            )

        rows = cursor.fetchall()
        conn.close()

        return [
            {"name": r[0], "date": r[1], "time": r[2], "confidence": r[3]}
            for r in rows
        ]

    def generate_report(self, output_path: str | Path | None = None) -> Path:
        if output_path is None:
            today = datetime.now().strftime("%Y-%m-%d")
            output_path = config.REPORTS_DIR / f"attendance_{today}.csv"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        records = self.get_attendance()

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "date", "time", "confidence"])
            writer.writeheader()
            writer.writerows(records)

        logger.info("Report generated: %s (%d entries)", output_path, len(records))
        return output_path

    def get_summary(self, date: str | None = None) -> dict:
        records = self.get_attendance(date)
        total = len(records)
        present = sum(1 for r in records if r["confidence"] > 0)
        return {
            "date": date or "all",
            "total": total,
            "present": present,
            "unknown": total - present,
        }
