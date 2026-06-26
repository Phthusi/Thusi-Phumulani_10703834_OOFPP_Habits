from ..habit_input import Habit_Inputs
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

from ...data.db_manager import CompleteHabit, Habits

class Add_Habit:
    def __init__(self,complete_habit:CompleteHabit):
        self.__habit = complete_habit

    def is_clashing_with_any_habit(self):
        habits = [Habits().get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])] 
        datetime1 = self.__habit.get_start_date()
        duration1 = self.__datetime_manager.convert_duration(self.__habit.get_session_duration())
        for habit in habits: 
            id, name, start_datetime, duration, status = habit
            datetime2 = self.__datetime_manager.string_to_datetime(start_datetime)
            duration2 = self.__datetime_manager.convert_duration(duration)
            if self.__datetime_manager.is_clashing(datetime1,duration1,datetime2,duration2):
                habit_from_db = f'Habit(id={id},name={name}, start_datetime={datetime2}, session_duration={duration}, status={status})'
                habit_to_be_added = f'Habit(id={self.__habit.get_id()}, name={self.__habit.get_name()}, start_datetime={datetime1}, session_duration={self.__habit.get_session_duration()})'
                return False, f'{habit_to_be_added} cannot be saved beacuse it clashes with {habit_from_db}'

    def save(self):
        return self.__habit.save_habit()



