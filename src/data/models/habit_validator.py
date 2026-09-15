from ...components.time_project.time_manager_validator import HabitDateTimeManagerValidator
from ...components.ui.read_json import read_json_files
class HabitValidator:
    '''
    Validates habit values before they are saved in the database
    '''
    def __init__(self, habit):
        self.habit = habit
        self.__time_manager_validator = HabitDateTimeManagerValidator()
        self.__statuses = read_json_files()['valid_statuses']
        self.__periodicities = read_json_files()['valid_periodicities']

    def set_habit(self,habit):
        self.habit = habit

    def valid_name(self):
        """
        Returns whether the habit has a name that is not:
        1. Empty
        2. Has 3 or more characters
        """
        min_name_length = 3
        name = self.habit.get_name()

        if name=="default":
            return False,"Name cannot be empty"
    
        if not isinstance(name, str):
            return False, "Name must be a string."

        if len(name) < min_name_length:
            return False, f"Name must be at least {min_name_length} characters long."

        return True, "name is valid."

    def valid_session_duration(self):
        """
        Validates the duration in 'HH:MM:SS' format
        """
        duration = self.habit.get_session_duration()

        if duration=="default":
            return False,"Duration cannot be empty"
    
        if not isinstance(duration, str):
            return False, "session datetime must be a string"

        message,success = self.__time_manager_validator.validate_duration(duration)
        if not success:
            return False, "Duration must use HH:MM:SS."
        
        return True, "session datetime is valid."

    def valid_status(self):
        '''Validate the habit status.'''
        if self.habit.get_status()=="default":
            return False,"Status cannot be empty"
    
        if self.habit.get_status() not in self.__statuses:
            return False, "Status must be one of: UPCOMING, IN_PROGRESS, COMPLETED, MISSED."
        return True, "status is valid."

    def valid_periodicity(self):
        '''Return the recurrence period.'''
        value = self.habit.get_periodicity()
        if value is not None and value not in self.__periodicities:
            return False,"Periodicity must be Daily, Weekly, or None."
        return True, "periodicity is valid"

    def valid_id(self):
        '''Validate the optional database ID.'''
        habit_id_is_none = self.habit.get_id() == None
        habit_id_is_int =  isinstance(self.habit.get_id(), int)
        if not habit_id_is_none and not habit_id_is_int:
            return False, "ID must be an integer or None."
        return True, "id is valid."
    
    def valid_for_updating(self):
        '''Return whether a habit is still editable.'''
        if self.habit.get_status() not in ["UPCOMING", "IN_PROGRESS"]:
            return False,"Habit cannot be updated because it has passed or it was completed"
        return True,"Habit can be updated"

    def valid_start_datetime(self):
        """Validate a scheduled datetime."""
        value = self.habit.get_start_date()

        if value == "default":
            return False, "Start datetime must not be empty."
    
        if not isinstance(value, str):
            return False, "Start datetime must be a datetime string."
        
        success = self.__time_manager_validator.is_datetime_valid
        if not success:
            return False, "Start datetime must use YYYY-MM-DD HH:MM:SS."
        return True, "start datetime is valid."

    def validate(self):
        '''Run all model validation rules and return "(valid,message)"'''
        validators = [
            self.valid_id,
            self.valid_name,
            self.valid_session_duration,
            self.valid_start_datetime,
            self.valid_status,
        ]

        for validator in validators:
            is_valid, message = validator()
            if not is_valid:
                return False, message

        return True, "Habit is valid."