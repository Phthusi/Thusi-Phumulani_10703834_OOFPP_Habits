from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message
from ...data.db_manager import CompleteHabit, Habits
from ..habit_input import Habit_Inputs
from colorama import Fore
from ..pipe import Pipe

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class SearchHabit(Habit_Inputs):
    def __init__(self):
        self.__is_habit_found_in_pipe = False
        self.__grabbed_habit_status = "No habit has been grabbed from the pipe, please grab a habit first"
        self.__fields_to_update_form = None
        self.__pipe = Pipe()

    def __my_input(self,message,history_file_name,commands,field_pair=None):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"Home/SearchHabit/{modified_history_file_name}",field_pair=field_pair).lower()

    @retry_until_success
    def find_habits(self,message):
        commands = ['sort','get habits','save','grab habit','filter results','view']
        history_file_name = 'find_habit'
        habit_field_number = self.__my_input(message,history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        return True,'hello'
    
    @retry_until_success
    def sort_results(self,message):
        commands = ['asc','desc']
        history_file_name = 'sort_results'
        habit_field_number = self.__my_input(message,history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        return True,'hello'
    
    @retry_until_success
    def sort_by(self,message):
        commands = ['name','datetime','status','duration']
        history_file_name = 'sort_by'
        habit_field_number = self.__my_input(message,history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        return True,'hello'

    @retry_until_success
    def sort_by_name(self):
        pass

    @retry_until_success
    def sort_by_datetime(self):
        pass

    @retry_until_success
    def sort_by_status(self):
        pass

    @retry_until_success
    def filter(self):
        pass

    @retry_until_success
    def filter_by_name(self):
        pass
