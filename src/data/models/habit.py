"""Domain model for habits."""


class Habit:
    """Represent one scheduled habit session.

    The class intentionally remains small because persistence and user
    interaction are handled by the surrounding application layers.
    """

    def __init__(self, name: str, session_duration: str, start_date,
                 status: str = "UPCOMING", id = None,
                 periodicity = "DAILY"):
        """Create a habit with its scheduling and tracking information."""
        self.__name = name
        self.__session_duration = session_duration
        self.__start_date = start_date
        self.__status = status
        self.__id = id
        self.__periodicity = periodicity

    def set_periodicity(self, periodicity) -> None:
        """Set the recurrence period, for example ``DAILY`` or ``WEEKLY``."""
        self.__periodicity = periodicity

    def get_periodicity(self):
        """Return the recurrence period."""
        return self.__periodicity

    def get_name(self):
        """Return the habit name."""
        return self.__name

    def get_session_duration(self):
        """Return the planned session duration as ``HH:MM:SS``."""
        return self.__session_duration

    def get_start_date(self):
        """Return the scheduled start date/time."""
        return self.__start_date

    def get_status(self):
        """Return the current habit status."""
        return self.__status

    def get_id(self):
        """Return the database identifier, if assigned."""
        return self.__id

    def set_name(self, name):
        """Set the habit name."""
        self.__name = name

    def set_session_duration(self, session_duration):
        """Set the planned session duration."""
        self.__session_duration = session_duration

    def set_start_date(self, start_date):
        """Set the scheduled start date/time."""
        self.__start_date = start_date

    def set_status(self, status):
        """Set the habit status."""
        self.__status = status

    def __str__(self):
        """Return a readable representation of the habit."""
        return (f"Habit(id={self.__id}, name='{self.__name}', "
                f"session_duration='{self.__session_duration}', "
                f"start_date='{self.__start_date}', status='{self.__status}', "
                f"periodicity='{self.__periodicity}')")
