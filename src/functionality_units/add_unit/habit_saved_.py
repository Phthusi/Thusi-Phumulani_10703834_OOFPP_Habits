from ...data.db_manager import CompleteHabit, Habits
from ..ui.command_autocomplete import AutoCompleter
from ..time_project.time_manager import HabitDateTimeManager
from ..time_project.time_manager_validator import HabitDateTimeManagerValidator
from ..ui.terminal_utils import ran_common_functions, retry_until_success

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class AddHabit:
    def __init__(self):
        self.__habit = CompleteHabit()
        self.__datetime_manager = HabitDateTimeManager()
        self.__datetime_validator = HabitDateTimeManagerValidator()

    def __set_habit_name(self,message):
        history_file_name='habit_name'
        commands = []
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        return autocompleter.prompt_input(message)
    
    @retry_until_success
    def set_habit_name(self,message):
        habit_name = self.__set_habit_name(message)

        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(habit_name)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        
        return self.__habit.set_name(habit_name)

    def __set_habit_start_datetime(self,message):
        history_file_name='start_datetime'
        commands = []
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        return autocompleter.prompt_input(message,[],'format: yyyy-mm-dd, HH:MM e.g 2026-06-08, 08:53')


    @retry_until_success
    def set_start_datetime(self,message):
        habit_start_datetime = self.__set_habit_start_datetime(message)
        
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_start_datetime)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************

        if not self.__datetime_validator.is_date_valid(habit_start_datetime):
            return False, 'Invalid format'
        
        if not self.__datetime_validator.is_passed(habit_start_datetime):
            return False, 'You cannot schedule for the time that has passed'

        self.__habit.set_start_date(self.__datetime_manager.string_to_datetime(habit_start_datetime))
        return True, 'valid start datetime'

    def __set_habit_session_duration(self,message,example=None):
        history_file_name='session_duration'
        commands = []
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        return autocompleter.prompt_input(message,example)
    
    @retry_until_success
    def set_session_duration(self,message):
        habit_session_duration = self.__set_habit_session_duration(message)

        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_session_duration)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************

        if not self.__datetime_validator.is_time_format_valid(habit_session_duration):
            return False, 'Invalid format'
        
        self.__habit.set_session_duration(habit_session_duration)
        return True, 'valid start datetime'

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

