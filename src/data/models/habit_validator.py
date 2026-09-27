"""Validation rules for the habit domain model."""

from datetime import datetime
from ...components.ui.terminal_utils import trace_call

class HabitValidator:
    """Validate habit values before they reach the persistence layer."""

    VALID_STATUSES = {"UPCOMING", "ONGOING", "IN_PROGRESS", "TO_BE_CONFIRMED",
                      "COMPLETED", "MISSED", "UNKNOWN"}
    VALID_PERIODICITIES = {"DAILY", "WEEKLY"}

    def __init__(self, habit):
        """Create a validator for ``habit``."""
        self.habit = habit

    def set_habit(self,habit):
        self.habit = habit

    @trace_call
    def valid_name(self):
        """Return whether the habit has a non-empty name of at least 3 characters."""
        name = self.habit.get_name()
        if not isinstance(name, str):
            return False, "Name must be a string."
        if not name.strip() or name == "default":
            return False, "Name cannot be empty."
        if len(name.strip()) < 3:
            return False, "Name must be at least 3 characters long."
        return True, "name is valid."

    @trace_call
    def valid_session_duration(self):
        """Validate a duration in ``HH:MM:SS`` format."""
        duration = self.habit.get_session_duration()
        if not isinstance(duration, str) or duration == "default":
            return False, "Session duration must be a string."
        try:
            hours, minutes, seconds = map(int, duration.split(":"))
            if hours < 0 or hours >= 24 or not 0 <= minutes < 60 or not 0 <= seconds < 60:
                raise ValueError
        except (ValueError, TypeError):
            return False, "Session duration must use HH:MM:SS with valid values."
        return True, "session duration is valid."

    @trace_call
    def valid_start_date(self):
        """Validate a scheduled datetime."""
        value = self.habit.get_start_date()
        if isinstance(value, datetime):
            return True, "start datetime is valid."
        if not isinstance(value, str) or value == "default":
            return False, "Start datetime must be a datetime or a datetime string."
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return False, "Start datetime must use YYYY-MM-DD HH:MM:SS."
        return True, "start datetime is valid."

    @trace_call
    def valid_status(self):
        """Validate the habit status."""
        if self.habit.get_status() not in self.VALID_STATUSES:
            return False, f"Status must be one of: {', '.join(sorted(self.VALID_STATUSES))}."
        return True, "status is valid."

    @trace_call
    def valid_periodicity(self):
        """Validate daily/weekly recurrence when one is supplied."""
        value = self.habit.get_periodicity()
        if value is not None and value not in self.VALID_PERIODICITIES:
            return False, "Periodicity must be DAILY, WEEKLY, or None."
        return True, "periodicity is valid."

    @trace_call
    def valid_id(self):
        """Validate the optional database ID."""
        if self.habit.get_id() is not None and not isinstance(self.habit.get_id(), int):
            return False, "ID must be an integer or None."
        return True, "id is valid."

    @trace_call
    def valid_for_updating(self):
        """Return whether a habit is still editable."""
        if self.habit.get_status() not in {"UPCOMING", "ONGOING", "IN_PROGRESS", "TO_BE_CONFIRMED"}:
            return False, "Habit cannot be updated because it has passed or was completed."
        return True, "Habit can be updated."

    @trace_call
    def validate(self):
        """Run all model validation rules and return ``(valid, message)``."""
        for validator in (self.valid_id, self.valid_name, self.valid_session_duration,
                          self.valid_start_date, self.valid_status, self.valid_periodicity):
            is_valid, message = validator()
            if not is_valid:
                return False, message
        return True, "Habit is valid."
