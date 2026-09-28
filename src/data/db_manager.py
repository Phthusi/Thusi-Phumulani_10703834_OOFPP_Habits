"""High-level habit model and collection operations."""

from datetime import datetime
from .models.habit import Habit
from .models.habit_validator import HabitValidator
from .db_functionality.db_interface import DB_Interface


class CompleteHabit(Habit):
    """Habit model with validation and persistence operations."""

    def __init__(self, name="default", session_duration="default", start_date="default",
                 status="UPCOMING", id=None, periodicity="DAILY"):
        """Create a persistence-aware habit."""
        super().__init__(name, session_duration, start_date, status, id, periodicity)
        self.__validator = HabitValidator(self)
        self.__db_interface = DB_Interface()

    def save_habit(self):
        """Validate and persist this habit."""
        valid, message = self.__validator.validate()
        if not valid:
            return valid, message
        self.__db_interface.set_is_db_updated(True)
        return self.__db_interface.add_habit(
            self.get_name(), self.get_start_date(), self.get_session_duration(),
            self.get_status(), self.get_periodicity())

    def update_habit(self, **kwargs):
        """Update editable database fields for this habit."""
        if self.get_id() is None:
            return False, "Habit has no id"
        valid, message = self.__validator.valid_id()
        if not valid:
            return valid, message
        valid, message = self.__validator.valid_for_updating()
        if not valid:
            return valid, message
        self.__db_interface.set_is_db_updated(True)
        return self.__db_interface.update_habit(self.get_id(), **kwargs)

    def complete_habit(self, **kwargs):
        """Mark a pending session as completed."""
        if self.get_id() is None:
            return False, "Habit has no id"
        valid, message = self.__validator.valid_id()
        if not valid:
            return valid, message
        if self.get_status() != "TO_BE_CONFIRMED":
            return False, "This habit's status does not allow for it to be completed"
        self.__db_interface.set_is_db_updated(True)
        return self.__db_interface.update_habit(self.get_id(), status="COMPLETED")

    def copy_habit(self):
        """Return an unsaved copy of this habit."""
        return CompleteHabit(self.get_name(), self.get_session_duration(), self.get_start_date(),
                             self.get_status(), periodicity=self.get_periodicity())

    def delete_habit(self):
        """Delete this habit from persistent storage."""
        if self.get_id() is None:
            return False, "Habit has no id"
        valid, message = self.__validator.valid_id()
        if not valid:
            return valid, message
        
        self.__db_interface.set_is_db_updated(True)
        return self.__db_interface.delete_habit(self.get_id())

    def set_name(self, name):
        """Set the name only when it passes validation."""
        old = self.get_name()
        super().set_name(name)
        valid, message = self.__validator.valid_name()
        if not valid:
            super().set_name(old)
        return valid, message

    def clear_name(self):
        super().set_name('default')

    def set_session_duration(self, duration):
        """Set the duration only when it is valid."""
        old = self.get_session_duration()
        super().set_session_duration(duration)
        valid, message = self.__validator.valid_session_duration()
        if not valid:
            super().set_session_duration(old)
        return valid, message

    def clear_session_duration(self):
        super().set_session_duration('default')

    def set_start_date(self, start_date):
        """Set the start date only when it is valid."""
        old = self.get_start_date()
        super().set_start_date(start_date)
        valid, message = self.__validator.valid_start_date()
        if not valid:
            super().set_start_date(old)
        return valid, message

    def clear_start_date(self):
        super().set_start_date('default')

    def set_status(self, status):
        """Set the status only when it is valid."""
        old = self.get_status()
        super().set_status(status)
        valid, message = self.__validator.valid_status()
        if not valid:
            super().set_status(old)
        return valid, message

    def set_periodicity(self, periodicity):
        """Set the recurrence period only when it is valid."""
        old = self.get_periodicity()
        super().set_periodicity(periodicity)
        valid, message = self.__validator.valid_periodicity()
        if not valid:
            super().set_periodicity(old)
        return valid, message

    def set_id(self, habit_id):
        """Set the database ID only when it is an integer or ``None``."""
        old = self.get_id()
        self._Habit__id = habit_id
        valid, message = self.__validator.valid_id()
        if not valid:
            self._Habit__id = old
        return valid, message


class Habits:
    """Collection/query facade for stored habit sessions."""

    def __init__(self, database_name=None):
        """Create a habit collection backed by ``database_name`` when supplied."""
        self.__db_interface = DB_Interface(database_name)

    def get_habits(self):
        """Return all stored habit tuples."""
        return self.__db_interface.get_cached_data()

    def id_is_available(self, habit_id):
        """Return whether a habit ID exists."""
        return any(entry[0] == habit_id for entry in self.get_habits())

    def get_habit_before_time(self, time):
        """Return sessions scheduled before a clock time."""
        return [h for h in self.get_habits() if h[2].split(" ")[1] < time]

    def get_habit_after_time(self, time):
        """Return sessions scheduled after a clock time."""
        return [h for h in self.get_habits() if h[2].split(" ")[1] > time]

    def get_habit_exactly_at(self, time):
        """Return sessions scheduled exactly at a clock time."""
        return [h for h in self.get_habits() if h[2].split(" ")[1] == time]

    def get_habit_exactly_at_date(self, date):
        """Return sessions scheduled on an exact calendar date."""
        return [h for h in self.get_habits() if h[2].split(" ")[0] == date]

    def get_habit_by_date(self, date):
        """Return sessions occurring on ``date``."""
        return self.get_habit_exactly_at_date(date)

    def get_habit_by_name(self, name):
        """Return habits whose name exactly matches ``name``."""
        return list(filter(lambda habit: name == habit[1], self.get_habits()))

    def get_habit_by_has_name(self, name):
        """Return habits whose name contains ``name``."""
        return list(filter(lambda habit: name in habit[1], self.get_habits()))

    def get_habit_by_status(self, status):
        """Return habits with the requested status."""
        return list(filter(lambda habit: status == habit[4], self.get_habits()))

    def get_habit_by_status_excluding_some_statuses(self, statuses):
        """Return habits whose status is not in ``statuses``."""
        return list(filter(lambda habit: habit[4] not in statuses, self.get_habits()))

    def get_habit_by_id(self, habit_id):
        """Return the habit with ``habit_id`` as a one-item list."""
        return list(filter(lambda habit: habit_id == habit[0], self.get_habits()))

    def get_habit_before_date(self, date):
        """Return sessions before a calendar date."""
        return [h for h in self.get_habits() if h[2].split(" ")[0] < date]

    def get_habit_after_date(self, date):
        """Return sessions after a calendar date."""
        return [h for h in self.get_habits() if h[2].split(" ")[0] > date]

    def get_habits_on_and_after_date(self, date, habits=None):
        """Return supplied habits, or all habits, on/after ``date``."""
        source = self.get_habits() if habits is None else habits
        return [h for h in source if h[2].split(" ")[0] >= date]

    def get_habit_between_dates(self, start_date, end_date):
        """Return sessions strictly between two calendar dates."""
        return [h for h in self.get_habits() if start_date < h[2].split(" ")[0] < end_date]

    def get_by_duration(self, duration):
        """Return sessions with an exact duration."""
        return [h for h in self.get_habits() if h[3] == duration]

    def get_by_duration_between(self, start_duration, end_duration):
        """Return sessions whose durations fall within the supplied range."""
        return [h for h in self.get_habits() if start_duration < h[3] < end_duration]

    def get_by_duration_greater_than(self, duration):
        """Return sessions longer than ``duration``."""
        return [h for h in self.get_habits() if h[3] > duration]

    def get_by_duration_less_than(self, duration):
        """Return sessions shorter than ``duration``."""
        return [h for h in self.get_habits() if h[3] < duration]

    def get_upcoming_and_date_before(self, date):
        """Return upcoming habits scheduled on/after ``date``."""
        return self.get_habits_on_and_after_date(date, self.get_habit_by_status("UPCOMING"))
