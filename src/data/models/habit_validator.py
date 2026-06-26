from datetime import datetime,timedelta

class HabitValidator:
    def __init__(self, habit):
        self.habit = habit
    
    def valid_name(self):
        min_name_length = 3
        if self.habit.get_name()=="default":
            return False,"Name cannot be empty"
    
        if not isinstance(self.habit.get_name(), str):
            return False, "Name must be a string."

        if len(self.habit.get_name()) < min_name_length:
            return False, f"Name must be at least {min_name_length} characters long."

        return True, "name is valid."

    def valid_session_duration(self):
        if self.habit.get_session_duration()=="default":
            return False,"Name cannot be empty"
    
        if not isinstance(self.habit.get_session_duration(), str):
            return False, "session datetime must be a datetime object"
        
        return True, "session datetime is valid."

    def valid_status(self):
        if self.habit.get_status()=="default":
            return False,"Name cannot be empty"
    
        if self.habit.get_status() not in ["UPCOMING", "IN_PROGRESS", "COMPLETED", "MISSED"]:
            return False, "Status must be one of: UPCOMING, IN_PROGRESS, COMPLETED, MISSED."
        return True, "status is valid."

    def valid_id(self):
        if self.habit.get_id() is not None and not isinstance(self.habit.get_id(), int):
            return False, "ID must be an integer or None."

        return True, "id is valid."
    
    def valid_for_updating(self):
        if self.habit.get_status() not in ["UPCOMING", "IN_PROGRESS"]:
            return False,"Habit cannot be updated because it has passed or it was completed"
        return True,"Habit can be updated"

    def validate(self):
        validators = [
            self.valid_id,
            self.valid_name,
            self.valid_session_duration,
            self.valid_status,
        ]

        for validator in validators:
            is_valid, message = validator()
            if not is_valid:
                return False, message

        return True, "Habit is valid."
                