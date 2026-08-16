from pathlib import Path
from typing import Any, List, Optional, Tuple, Union
from .db import Database


class DB_Interface:
    """Caching abstraction layer sitting over the low-level SQLite Database.

    Maintains an in-memory cache of habits to minimize raw database query overhead.
    """

    __cached_data: List[Tuple[Any, ...]] = []
    is_db_updated = False

    def __init__(
        self,
        database_name: Union[str, Path] = Path(__file__).resolve().parent.parent.parent.parent / "habit.db",
    ) -> None:
        """Initialize DB connection and warm up the in-memory cache.

        Args:
            database_name (Union[str, Path]): Path to database file.
        """
        self.__db = Database(str(database_name))
        self.get_all_habits()

    def __id_in_db(self, habit_id: int) -> bool:
        """Check if a given ID currently exists in the local cache.

        Args:
            habit_id (int): Primary key to verify.

        Returns:
            bool: True if ID exists in cache, False otherwise.
        """
        return habit_id in [entry[0] for entry in self.__cached_data]

    def get_all_habits(self) -> List[Tuple[Any, ...]]:
        """Refresh local cache from database and return all habit tuples.

        Returns:
            List[Tuple[Any, ...]]: Cached habit tuples.
        """
        _, self.__cached_data = self.__db.get_all_habits()
        return self.__cached_data

    @classmethod
    def set_is_db_updated(cls,is_db_updated):
        cls.is_db_updated = is_db_updated

    def update_habit(self, habit_id: int, **kwargs: Any) -> Tuple[str, str]:
        """Update a habit in database and refresh cache on success.

        Args:
            habit_id (int): Primary key of target habit.
            **kwargs (Any): Fields to update.

        Returns:
            Tuple[str, str]: Status ('success' or 'error') and result message.
        """
        if self.__id_in_db(habit_id):
            success, message = self.__db.update_habit(habit_id, **kwargs)
            self.get_all_habits()
            return success, message
        return "error", f"habit with id={habit_id} does not exist"

    def add_habit(
        self,
        name: str,
        start_datetime: str,
        duration: str,
        status: str,
        periodicity: Optional[str] = None,
    ) -> Tuple[str, Any]:
        """Add a habit to the database and update the local cache immediately.

        Args:
            name (str): Title of the habit.
            start_datetime (str): Scheduled start time string.
            duration (str): Session duration.
            status (str): Initial state (e.g. 'UPCOMING').
            periodicity (Optional[str]): Recurrence period.

        Returns:
            Tuple[str, Any]: Status ('success' or 'error') and newly generated ID or error details.
        """
        success, habit_id = self.__db.add_habit(name, start_datetime, duration, status, periodicity)
        if success == "success":
            self.__cached_data.append((habit_id, name, start_datetime, duration, status, periodicity))
        return success, habit_id

    def delete_habit(self, habit_id: int) -> Tuple[str, Optional[str]]:
        """Remove habit from database and purge from in-memory cache.

        Args:
            habit_id (int): Primary key ID to delete.

        Returns:
            Tuple[str, Optional[str]]: Status ('success' or 'error') and result message.
        """
        if not self.__id_in_db(habit_id):
            return "error", f"habit with id={habit_id} does not exist"
        success, result = self.__db.delete_habit(habit_id)
        if success == "success":
            self.__cached_data = [entry for entry in self.__cached_data if entry[0] != habit_id]
        return success, result

    def get_cached_data(self) -> List[Tuple[Any, ...]]:
        """Return raw cached habit records without hitting the database.

        Returns:
            List[Tuple[Any, ...]]: Current list of cached habit tuples.
        """
        if self.is_db_updated:
            self.get_all_habits()
            self.is_db_updated = False
        return self.__cached_data

if __name__ == "__main__":
    interface = DB_Interface()
    print(interface.get_all_habits())