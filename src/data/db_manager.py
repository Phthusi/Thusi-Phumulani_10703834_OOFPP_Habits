from .models.habit import Habit
from .models.habit_validator import HabitValidator
from .db_functionality.db_interface import DB_Interface

class CompleteHabit(Habit):     
    """Habit model with validation and persistence operations."""

    def __init__(self, name="default", session_duration="default", start_date="default", status="UPCOMING", id=None):
        """Create a persistence-aware habit."""
        super().__init__(name, session_duration, start_date, status, id)
        self.__validator = HabitValidator(self)
        self.__db_interface = DB_Interface()
    
    def save_habit(self):
        """Validate and persist this habit."""
        is_valid_habit, message = self.__validator.validate()
        if not is_valid_habit:
            return is_valid_habit,message
        
        name = self.get_name()
        start_datetime = self.get_start_date()
        duration = self.get_session_duration()
        status = self.get_status()
        periodicity = self.get_periodicity()
        success, id = self.__db_interface.add_habit(name,start_datetime,duration,status,periodicity)
        return  success, id

    def update_habit(self,**kwargs):
        """Update editable database fields for this habit."""
        if self.get_id() == None:
            return False, "Habit has no id"

        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            return is_id_valid,message
        
        can_habit_be_updated,message = self.__validator.valid_for_updating()
        if not can_habit_be_updated:
            return can_habit_be_updated,message
        
        self.__db_interface.set_is_db_updated(True)
        return self.__db_interface.update_habit(self.get_id(),**kwargs)
    
    def complete_habit(self,**kwargs):
        """Mark a pending session as completed."""
        if self.get_id() == None:
            return False, "Habit has no id"

        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            return is_id_valid,message
        
        if self.get_status()!='TO_BE_CONFIRMED':
            return False, f'This habit\'s status does not allow for it to be completed'
        self.__db_interface.set_is_db_updated(True)
        return self.__db_interface.update_habit(habit_id=self.get_id(),**{'status':'COMPLETED'})

    def copy_habit(self):
        """Return an unsaved copy of this habit."""
        return CompleteHabit(self.get_name(), self.get_session_duration(), self.get_start_date(), self.get_status(),periodicity=self.get_periodicity())

    def delete_habit(self):
        """Delete this habit from persistent storage."""
        if self.get_id() is None:
            return False, "Habit has no id"

        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            return is_id_valid,message
        
        return self.__db_interface.delete_habit(self.get_id())

    def set_name(self, name):
        """Set the name only when it passes validation."""
        old_name = self.get_name()
        super().set_name(name)
        is_name_valid,message = self.__validator.valid_name()
        if not is_name_valid:
            super().set_name(old_name)
        return is_name_valid, message

    def set_session_duration(self, session_duration):
        """Set the duration only when it is valid."""
        old_session_duration = self.get_session_duration()
        super().set_session_duration(session_duration)
        is_session_duration_valid,message = self.__validator.valid_session_duration()
        if not is_session_duration_valid:
            super().set_session_duration(old_session_duration)
        return is_session_duration_valid, message
    
    def set_start_date(self, start_date):
        """Set the start date only when it is valid."""
        old = self.get_start_date()
        super().set_start_date(start_date)
        valid, message = self.__validator.valid_start_date()
        if not valid:
            super().set_start_date(old)
        return valid, message
    
    def set_status(self, status):
        """Set the status only when it is valid."""
        old_status = self.get_status()
        super().set_status(status)
        is_status_valid,message = self.__validator.valid_status()
        if not is_status_valid:
            super().set_status(old_status)
        return is_status_valid, message
    
    def set_id(self,id):
        """Set the database ID only when it is an integer or ``None``."""
        old_id = self.get_id()
        super().set_id(id)
        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            super().set_id(old_id)
        return is_id_valid, message

    def set_periodicity(self, periodicity):
        """Set the recurrence period only when it is valid."""
        old = self.get_periodicity()
        super().set_periodicity(periodicity)
        valid, message = self.__validator.valid_periodicity()
        if not valid:
            super().set_periodicity(old)
        return valid, message

class Habits:
    """Collection/query facade for stored habit sessions."""

    def __init__(self):
        """Create a habit collection backed by ``database_name`` when supplied."""
        self.__db_interface = DB_Interface()
    
    def get_habits(self):
        """Return all stored habit tuples."""
        return self.__db_interface.get_cached_data()

    def id_is_available(self,id):
        """Return whether a habit ID exists."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return len([entry for entry in self.__cached_data if entry[0]==id])==1

    def get_habit_before_time(self,time):
        """Return sessions scheduled before a clock time."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.__cached_data
        results = []
        for habit in habits:
            id,name,datetime,duration,status,periodicity = habit
            habit_date,habit_time = datetime.split(' ')
            if habit_time<time:
                results.append(habit)
        return results
    
    def get_habit_after_time(self,time):
        """Return sessions scheduled after a clock time."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.__cached_data
        results = []
        for habit in habits:
            id,name,datetime,duration,status,periodicity = habit
            habit_date,habit_time = datetime.split(' ')
            if habit_time>time:
                results.append(habit)
        return results

    def get_habit_exactly_at(self,time):
        """Return sessions scheduled exactly at a clock time."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.__cached_data
        results = []
        for habit in habits:
            id,name,datetime,duration,status,periodicity = habit
            habit_date,habit_time = datetime.split(' ')
            if habit_time==time:
                results.append(habit)
        return results

    def get_habit_exactly_at_date(self,date):
        """Return sessions scheduled on an exact calendar date."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.__cached_data
        results = []
        for habit in habits:
            id,name,datetime,duration,status,periodicity = habit
            habit_date,habit_time = datetime.split(' ')
            if habit_date==date:
                results.append(habit)
        return results

    def get_habit_by_date(self, date):
        """Return sessions occurring on ``date``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.__cached_data
        return [target_habit for target_habit in habits if date in target_habit[2]]
    
    def get_habit_by_name(self,name):
        """Return habits whose name exactly matches ``name``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:name==habit[1],self.__cached_data))
    
    def get_habit_by_has_name(self,name):
        """Return habits whose name contains ``name``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:name in habit[1],self.__cached_data)) 

    def get_habit_by_status(self,status):
        """Return habits with the requested status."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:status==habit[4],self.__cached_data))
    
    def get_habit_by_status_excluding_some_statuses(self,statuses):
        """Return habits whose status is not in ``statuses``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[4] not in statuses,self.__cached_data))

    def get_habit_by_id(self,id):
        """Return the habit with ``habit_id`` as a one-item list."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:id==habit[0],self.__cached_data))
    
    def get_habit_before_date(self,date):
        """Return sessions before a calendar date."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[2]<date,self.__cached_data))
    
    def get_habit_after_date(self,date):
        """Return sessions after a calendar date."""
        self.__cached_data = self.__db_interface.get_cached_data() 
        return list(filter(lambda  habit:habit[2]>date,self.__cached_data))
    
    def get_habits_on_and_after_date(self,date,habits=[]):
        """Return supplied habits, or all habits, on/after ``date``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.__cached_data if habits == [] else habits
        return list(filter(lambda  habit:habit[2]>=date,habits))

    def get_habit_between_dates(self,start_date,end_date):
        """Return sessions strictly between two calendar dates."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[2]>start_date and habit[2]<end_date,self.__cached_data))
    
    def get_by_duration(self,duration):
        """Return sessions with an exact duration."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[3]==duration,self.__cached_data))

    def get_by_duration_between(self,start_duration,end_duration):
        """Return sessions whose durations fall within the supplied range."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[3]>start_duration and habit[1]<end_duration,self.__cached_data))

    def get_by_duration_greater_than(self,duration):
        """Return sessions longer than ``duration``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[3]>duration,self.__cached_data))

    def get_by_duration_less_than(self,duration):
        """Return sessions shorter than ``duration``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        return list(filter(lambda  habit:habit[3]<duration,self.__cached_data))
    
    def get_upcoming_and_date_before(self,date):
        """Return upcoming habits scheduled on/after ``date``."""
        self.__cached_data = self.__db_interface.get_cached_data()
        habits = self.get_habit_by_status('UPCOMING')
        return self.get_habits_on_and_after_date(date,habits)