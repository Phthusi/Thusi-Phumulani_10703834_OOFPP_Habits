"""SQLite persistence for habit records."""

import sqlite3
from datetime import datetime


class Database:
    """Small SQLite repository used by the habit tracker."""

    VALID_FIELDS = {"name", "start_datetime", "duration", "status", "periodicity"}

    def __init__(self, db_name):
        """Open ``db_name`` and create the habit table when necessary."""
        self.__name = str(db_name)
        self.__connect = sqlite3.connect(self.__name)
        self.__connect.execute("PRAGMA foreign_keys = ON")
        self.__cursor = self.__connect.cursor()
        self.__create_table()

    def __create_table(self):
        """Create the habit table if it does not already exist."""
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                start_datetime TEXT NOT NULL,
                duration TEXT NOT NULL,
                status TEXT NOT NULL,
                periodicity TEXT
            )
        """)
        self.__connect.commit()

    @staticmethod
    def _normalise_datetime(value):
        """Convert a datetime object to the string representation used in SQLite."""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)

    def add_habit(self, name, start_datetime, duration, status, periodicity=None):
        """Insert a habit and return ``('success', id)`` or an error tuple."""
        try:
            self.__cursor.execute(
                "INSERT INTO habit (name, start_datetime, duration, status, periodicity) VALUES (?, ?, ?, ?, ?)",
                (name, self._normalise_datetime(start_datetime), duration, status, periodicity),
            )
            self.__connect.commit()
            return "success", self.__cursor.lastrowid
        except sqlite3.Error as exc:
            self.__connect.rollback()
            return "error", str(exc)

    def get_all_habits(self):
        """Return all habit rows ordered by their scheduled time."""
        try:
            self.__cursor.execute("SELECT id, name, start_datetime, duration, status, periodicity FROM habit ORDER BY start_datetime, id")
            return "success", self.__cursor.fetchall()
        except sqlite3.Error as exc:
            return "error", str(exc)

    def delete_habit(self, habit_id):
        """Delete a habit by ID and report whether the operation succeeded."""
        try:
            self.__cursor.eAxecute("DELETE FROM habit WHERE id = ?", (habit_id,))
            self.__connect.commit()
            if self.__cursor.rowcount == 0:
                return "error", f"habit with id={habit_id} does not exist"
            return "success", None
        except sqlite3.Error as exc:
            self.__connect.rollback()
            return "error", str(exc)

    def update_habit(self, habit_id, **kwargs):
        """Update allowed habit columns using parameterised SQL."""
        if not kwargs:
            return "error", "No fields supplied for update."
        if not set(kwargs).issubset(self.VALID_FIELDS):
            return "error", f"Invalid fields for habit table. Valid fields are: {self.VALID_FIELDS}"
        try:
            assignments = ", ".join(f"{field} = ?" for field in kwargs)
            values = [self._normalise_datetime(v) if field == "start_datetime" else v
                      for field, v in kwargs.items()]
            values.append(habit_id)
            self.__cursor.execute(f"UPDATE habit SET {assignments} WHERE id = ?", values)
            self.__connect.commit()
            if self.__cursor.rowcount == 0:
                return "error", f"habit with id={habit_id} does not exist"
            return "success", f"habit Habit(id={habit_id},) has been updated successfully..."
        except sqlite3.Error as exc:
            self.__connect.rollback()
            return "error", str(exc)

    def close(self):
        """Close the SQLite connection."""
        self.__connect.close()
