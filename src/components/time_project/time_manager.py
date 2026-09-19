"""Date, time and scheduling helpers used by the habit tracker."""

from datetime import datetime, timedelta


class HabitDateTimeManager:
    """Provide validation and scheduling calculations for habit sessions."""

    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def calculate_time_difference(self, start_time_str, end_time_str):
        """Return the elapsed time between two formatted datetimes."""
        if not self.is_date_valid(start_time_str) or not self.is_date_valid(end_time_str):
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
        return self.string_to_datetime(end_time_str) - self.string_to_datetime(start_time_str)

    def is_time_already_passed(self, datetime_to_check, now=None):
        """Return whether a scheduled datetime is at or before ``now``."""
        now = datetime.now() if now is None else now
        return self.string_to_datetime(datetime_to_check) <= now

    def is_clashing(self, datetime1, duration1, datetime2, duration2):
        """Return whether two sessions overlap in time."""
        end1 = datetime1 + duration1
        end2 = datetime2 + duration2
        return datetime1 < end2 and datetime2 < end1

    def determine_habit_status(self, start_dt_str: str, duration_str: str, now=None):
        """Determine session status from its start, duration and current time."""
        try:
            start_dt = self.string_to_datetime(start_dt_str)
            duration_td = self.convert_duration(duration_str)
            end_dt = start_dt + duration_td
            now = datetime.now() if now is None else now
            if start_dt > now:
                return "UPCOMING"
            if start_dt <= now < end_dt:
                return "ONGOING"
            if now <= end_dt + timedelta(days=1):
                return "TO_BE_CONFIRMED"
            return "MISSED"
        except (ValueError, TypeError):
            return "UNKNOWN"

    def convert_duration(self, duration_str):
        """Convert ``HH:MM:SS`` into a :class:`timedelta`."""
        hours, minutes, seconds = map(int, duration_str.split(":"))
        if hours < 0 or hours >= 24 or not 0 <= minutes < 60 or not 0 <= seconds < 60:
            raise ValueError("Invalid duration")
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def string_to_datetime(self, string_datetime):
        """Parse a tracker datetime string."""
        return datetime.strptime(string_datetime, self.DATETIME_FORMAT)

    def is_date_valid(self, value):
        """Return whether a full tracker datetime is valid."""
        try:
            self.string_to_datetime(value)
            return True
        except (ValueError, TypeError):
            return False

    def get_weekday(self, string_date):
        """Return a three-letter lowercase weekday name for a date."""
        return datetime.strptime(string_date, "%Y-%m-%d").strftime("%a").lower()

    def increase_by_day(self, string_date):
        """Return the next calendar date as ``YYYY-MM-DD``."""
        return (datetime.strptime(string_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
