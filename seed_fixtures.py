"""Load the five predefined four-week habit fixtures into SQLite."""

import json
from pathlib import Path

from src.data.db_functionality.db_interface import DB_Interface


ROOT = Path(__file__).resolve().parent
FIXTURE_FILE = ROOT / "fixtures" / "habits_fixture.json"


def seed(database_path=None):
    """Insert fixture sessions into ``database_path`` and return inserted IDs."""
    database = DB_Interface(database_path) if database_path else DB_Interface()
    with FIXTURE_FILE.open(encoding="utf-8") as handle:
        fixture = json.load(handle)

    inserted = []
    for habit in fixture["habits"]:
        for session in habit["sessions"]:
            result, habit_id = database.add_habit(
                habit["name"],
                session["date"],
                habit["duration"],
                session["status"],
                habit["periodicity"],
            )
            if result != "success":
                raise RuntimeError(habit_id)
            inserted.append(habit_id)
    return inserted


if __name__ == "__main__":
    ids = seed()
    print(f"Inserted {len(ids)} fixture sessions.")
