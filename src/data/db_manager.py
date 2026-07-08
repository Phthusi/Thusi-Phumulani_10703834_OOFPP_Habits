from .models.habit import Habit
from .models.habit_validator import HabitValidator
from .db_functionality.db_interface import DB_Interface

class CompleteHabit(Habit):     
    def __init__(self, name="default", session_duration="default", start_date="default", status="UPCOMING", id=None):
        super().__init__(name, session_duration, start_date, status, id)
        self.__validator = HabitValidator(self)
        self.__db_interface = DB_Interface()
    
    def save_habit(self):
        is_valid_habit, message = self.__validator.validate()
        if not is_valid_habit:
            return is_valid_habit,message
        
        name = self.get_name()
        start_datetime = self.get_start_date()
        duration = self.get_session_duration()
        status = self.get_status()

        return self.__db_interface.add_habit(name,start_datetime,duration,status)

    def update_habit(self,**kwargs):
        if self.get_id() == None:
            return False, "Habit has no id"

        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            return is_id_valid,message
        
        can_habit_be_updated,message = self.__validator.valid_for_updating()
        if not can_habit_be_updated:
            return can_habit_be_updated,message
        
        return self.__db_interface.update_habit(self.get_id(),**kwargs)

    def copy_habit(self):
        return CompleteHabit(self.get_name(), self.get_session_duration(), self.get_start_date(), self.get_status())

    def delete_habit(self):
        if self.get_id() == None:
            return False, "Habit has no id"

        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            return is_id_valid,message
        
        return self.__db_interface.delete_habit(self.get_id())

    def set_name(self, name):
        old_name = self.get_name()
        self._Habit__name = name
        is_name_valid,message = self.__validator.valid_name()
        if not is_name_valid:
            self._Habit__name = old_name
        return is_name_valid, message

    def set_session_duration(self, session_duration):
        old_session_duration = self.get_session_duration()
        self._Habit__session_duration = session_duration
        is_session_duration_valid,message = self.__validator.valid_session_duration()
        if not is_session_duration_valid:
            self._Habit__session_duration = old_session_duration
        return is_session_duration_valid, message
    
    def set_status(self, status):
        old_status = self.get_status()
        self._Habit__status = status
        is_status_valid,message = self.__validator.valid_status()
        if not is_status_valid:
            self._Habit__status = old_status
        return is_status_valid, message
    
    def set_id(self,id):
        old_id = self.get_id()
        self._Habit__id = id
        is_id_valid,message = self.__validator.valid_id()
        if not is_id_valid:
            self._Habit__id = old_id
        return is_id_valid, message


class Habits:
    def __init__(self):
        self.__cached_data = DB_Interface().get_cached_data()
    
    def get_habits(self):
        return self.__cached_data

    def id_is_available(self,id):
        return len([entry for entry in self.__cached_data if entry[0]==id])==1

    def get_habit_by_date(self, date):
        habits = self.__cached_data
        return [target_habit for target_habit in habits if date in target_habit[2]]
    
    def get_habit_by_name(self,name):
        return list(filter(lambda  habit:name==habit[1],self.__cached_data))
    
    def get_habit_by_status(self,status):
        return list(filter(lambda  habit:status==habit[4],self.__cached_data))
    
    def get_habit_by_status_excluding_some_statuses(self,statuses):
        return list(filter(lambda  habit:habit[4] not in statuses,self.__cached_data))

    def get_habit_by_id(self,id):
        return list(filter(lambda  habit:id==habit[0],self.__cached_data))
    
    def get_habit_before_date(self,date):
        return list(filter(lambda  habit:habit[2]<date,self.__cached_data))
    
    def get_habit_after_date(self,date):
        return list(filter(lambda  habit:habit[2]>date,self.__cached_data))
    
    def get_habits_on_and_after_date(self,date,habits=[]):
        habits = self.__cached_data if habits == [] else habits
        return list(filter(lambda  habit:habit[2]>=date,habits))

    def get_habit_between_dates(self,start_date,end_date):
        return list(filter(lambda  habit:habit[2]>start_date and habit[2]<end_date,self.__cached_data))
    
    def get_by_duration(self,duration):
        return list(filter(lambda  habit:habit[3]==duration,self.__cached_data))

    def get_by_duration_between(self,start_duration,end_duration):
        return list(filter(lambda  habit:habit[3]>start_duration and habit[1]<end_duration,self.__cached_data))

    def get_by_duration_greater_than(self,duration):
        return list(filter(lambda  habit:habit[3]>duration,self.__cached_data))

    def get_by_duration_less_than(self,duration):
        return list(filter(lambda  habit:habit[3]<duration,self.__cached_data))
    
    def get_upcoming_and_date_before(self,date):
        habits = self.get_habit_by_status('UPCOMING')
        return self.get_habits_on_and_after_date(date,habits)