import sys
from pathlib import Path
from typing import Optional


def parse_log_line(line: str) -> Optional[dict]:
    """
    Parse one log line of format:
    YYYY-MM-DD HH:MM:SS LEVEL Message...
    Returns dict or None if line is invalid.
    """
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        return None

    date, time, level, message = parts
    if not (date and time and level and message):
        return None

    return {"date": date, "time": time, "level": level.upper(), "message": message}


def load_logs(file_path: str) -> list[dict]:
    """
    Load logs from a file and parse each line.
    Skips invalid lines.
    """
    path = Path(file_path)
    logs: list[dict] = []

    try:
        with path.open("r", encoding="utf-8") as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
    except FileNotFoundError:
        raise FileNotFoundError("Log file not found.")
    except OSError as e:
        raise OSError(f"Error reading file: {e}")

    return logs


def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:
    """
    Filter logs by logging level (case-insensitive).
    """
    target = level.upper()
    return list(filter(lambda item: item.get("level") == target, logs))  # FP element: filter + lambda


def count_logs_by_level(logs: list[dict]) -> dict[str, int]:
    """
    Count log records by level.
    """
    counts: dict[str, int] = {}
    for item in logs:
        lvl = item.get("level", "UNKNOWN")
        counts[lvl] = counts.get(lvl, 0) + 1
    return counts


def display_log_counts(counts: dict[str, int]) -> None:
    """
    Display counts as a table.
    """
    header_left = "Рівень логування"
    header_right = "Кількість"

    print(f"{header_left:<16} | {header_right}")
    print("-" * 17 + "|" + "-" * 10)

    for level in sorted(counts.keys()):
        print(f"{level:<16} | {counts[level]}")


def display_log_details(logs: list[dict], level: str) -> None:
    """
    Display details for a chosen level.
    """
    target = level.upper()
    print(f"\nДеталі логів для рівня '{target}':")
    if not logs:
        print("Немає записів для цього рівня.")
        return

    for item in logs:
        print(f"{item['date']} {item['time']} - {item['message']}")


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Usage: python main.py <path_to_logfile> [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) == 3 else None

    try:
        logs = load_logs(file_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
        filtered = filter_logs_by_level(logs, level)
        display_log_details(filtered, level)


if __name__ == "__main__":
    main()
