"""Application-facing persistence interface with a small local cache."""

from pathlib import Path
from .db import Database


class DB_Interface:
    """Cache wrapper around :class:`Database`.

    The cache is instance-local so test databases and application sessions do not
    accidentally share state.
    """

    is_db_updated = False

    def __init__(self, database_name= None) -> None:
        """Open a database and load its current rows into the cache."""
        if database_name is None:
            database_name = Path(__file__).resolve().parents[3] / "habit.db"
        self.__db = Database(str(database_name))
        self.__cached_data = []
        self.get_all_habits()

    def __id_in_db(self, habit_id: int):
        """Return whether ``habit_id`` is present in the cache."""
        return any(entry[0] == habit_id for entry in self.__cached_data)

    def get_all_habits(self) :
        """Refresh and return all cached habit rows."""
        success, data = self.__db.get_all_habits()
        self.__cached_data = data if success == "success" else []
        return self.__cached_data

    @classmethod
    def set_is_db_updated(cls, is_db_updated):
        """Mark all interface instances for a cache refresh."""
        cls.is_db_updated = is_db_updated

    def update_habit(self, habit_id: int, **kwargs):
        """Update a habit and refresh the cache."""
        if not self.__id_in_db(habit_id):
            return "error", f"habit with id={habit_id} does not exist"
        result = self.__db.update_habit(habit_id, **kwargs)
        if result[0] == "success":
            self.get_all_habits()
        return result

    def add_habit(self, name: str, start_datetime: str, duration: str, status: str, periodicity = None):
        """Persist a habit and append it to the cache."""
        result = self.__db.add_habit(name, start_datetime, duration, status, periodicity)
        if result[0] == "success":
            self.get_all_habits()
        return result

    def delete_habit(self, habit_id: int):
        """Delete a habit and remove it from the cache."""
        if not self.__id_in_db(habit_id):
            return "error", f"habit with id={habit_id} does not exist"
        result = self.__db.delete_habit(habit_id)
        if result[0] == "success":
            self.get_all_habits()
        return result

    def get_cached_data(self) :
        """Return the current cache, refreshing it after a flagged update."""
        if self.is_db_updated:
            self.get_all_habits()
            self.is_db_updated = False
        return list(self.__cached_data)

    def close(self):
        """Close the underlying database connection."""
        self.__db.close()
