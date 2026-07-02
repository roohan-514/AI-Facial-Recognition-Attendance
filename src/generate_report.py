"""CLI script to generate attendance reports."""
import argparse
import sys
import logging

sys.path.insert(0, ".")

import config
from src.attendance_manager import AttendanceManager

logging.basicConfig(level=logging.INFO, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generate attendance report"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date in YYYY-MM-DD format (default: all dates)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV path (default: data/reports/attendance_<date>.csv)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary instead of full report",
    )
    args = parser.parse_args()

    manager = AttendanceManager()

    if args.summary:
        summary = manager.get_summary(args.date)
        print(f"Date:     {summary['date']}")
        print(f"Total:    {summary['total']}")
        print(f"Present:  {summary['present']}")
        print(f"Unknown:  {summary['unknown']}")
    else:
        path = manager.generate_report(args.output)
        records = manager.get_attendance(args.date)
        print(f"Report saved to: {path}")
        print(f"Total entries: {len(records)}")
        if records:
            print(f"{'Name':<20} {'Date':<12} {'Time':<10} {'Conf':<6}")
            print("-" * 48)
            for r in records:
                print(
                    f"{r['name']:<20} {r['date']:<12} {r['time']:<10} "
                    f"{r['confidence']:<6.2f}"
                )


if __name__ == "__main__":
    main()
