from datetime import datetime
from ...components.ui.terminal_utils import trace_call

class HabitDateTimeManagerValidator:
    """
    Validates and processes date, time, and duration strings for habit tracking.

    Provides utility methods to check date-time format correctness, parse 
    24-hour time values, compare timestamps against current time, and validate 
    duration strings.
    """
    @trace_call
    def is_datetime_valid(self, date_str):
        """
        Validates whether a string matches the 'YYYY-MM-DD HH:MM:SS' format.

        Args:
            date_str (str): Date and time string to validate.

        Returns:
            bool: True if the string is a valid datetime format, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
        
    @trace_call
    def is_date_valid(self, date_str):
        """
        Validates whether a string matches the 'YYYY-MM-DD' date format.

        Args:
            date_str (str): Date string to validate.

        Returns:
            bool: True if the string is a valid date format, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    @trace_call
    def is_passed(self,date_str):
        """
        Checks if a given datetime string is scheduled in the future relative to now.

        Args:
            date_str (str): Datetime string in 'YYYY-MM-DD HH:MM:SS' format.

        Returns:
            bool: True if the target datetime is greater than current local time,
                False otherwise.
        """
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") > datetime.now()

    @trace_call
    def is_time_format_valid(self, time_str):
        """
        Validates whether a string matches 24-hour time format ('HH:MM:SS').

        Args:
            time_str (str): Time string to validate.

        Returns:
            bool: True if hours (0-23), minutes (0-59), and seconds (0-59) 
                fall within valid ranges, False otherwise.
        """
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
                return True
            return False
        except Exception:
            return False

    def validate_duration(self,duration):
        """
        Validates a duration string formatted as 'HH:MM:SS' against bounds constraints.

        Args:
            duration (str): Duration string to evaluate.

        Returns:
            tuple[str, bool]: A tuple containing a status string ('SUCCESSFUL...' or
                'UNSUCCESSFUL...') and a boolean indicating validation success.
        """
        try:
            hours, minutes, seconds = map(int, duration.split(":"))
            assert 0<=hours<24, 'hours must be greater or equal to zero but it must be less than 24'
            assert 0<=minutes<60, 'Minutes must be greater or equal to zero but it must be less than 60'
            assert 0<=seconds<60 , 'Seconds must be greater or equal to zero but it must be less than 60'
            return "SUCCESSFUL: duration set", True

        except Exception as e:
            return f"UNSUCCESSFUL: {e}", False    
        