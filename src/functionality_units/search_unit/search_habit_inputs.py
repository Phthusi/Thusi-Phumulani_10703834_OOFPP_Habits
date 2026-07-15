from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message
from ...data.db_manager import CompleteHabit, Habits
from ..habit_input import Habit_Inputs 
from colorama import Fore
from ..shelf import Shelf

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class SearchHabitInputs(Habit_Inputs):
    def __init__(self):
        self.__number_of_habit_fields = None
        self.__field_names  = []
        self.__main_form = Form({field: False for field in ['id','number_of_habit_fields']})
        self.__fields_to_update_form = None
        self.__shelf = Shelf()
        self.__current_fields = dict()
        super().__init__(BASE_DIR)
        self.__habits = []
        self.__habit_search = Habits()
        self.__habit = None
        self.__searched_habits_status = "No habit search has been done yet, please search for habits first"

    def __my_input(self,message,history_file_name,commands,field_pair=None,base='Home/SearchHabit/'):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"{base}{modified_history_file_name}",field_pair=field_pair).lower()

    def get_main_form(self):
        return self.__main_form

    def display_grabbed_habit(self):
        if self.__habit==None:
            print(f'''{Fore.LIGHTBLACK_EX}Status          : ❌ {self.__searched_habits_status}
Shared Habit ID : {Fore.LIGHTBLUE_EX}N/A''')
            return
        print(f'''{Fore.LIGHTBLACK_EX}Status          : ✅ {self.__searched_habits_status}
Shared Habit ID : {Fore.LIGHTGREEN_EX}{self.__habit._Habit__id}''')

    @retry_until_success
    def handle_get_time(self):
        commands = ['time before','time at','time after']
        history_file_name = 'get_time'
        habit_field_number = self.__my_input('Choose blah blah blah: ',history_file_name,commands,base='Home/SearchHabit/FindHabit/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************

    @retry_until_success
    def handle_get_duration(self):
        pass

    @retry_until_success
    def handle_get_date(self):
        commands = ['find habit before','find habits after','find habits at']
        history_file_name = 'get_date'
        habit_field_number = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands)
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
    def handle_get_name(self):
        pass

    @retry_until_success
    def find_habits(self):
        commands = ['get by date','get by time','get by duration','get by name','get by status','get by id']
        history_file_name = 'find_habit'
        habit_field_number = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        command_functions = {
            'get by date':self.handle_get_date,
            'get by time':self.handle_get_time,
            'get by duration':self.handle_get_duration,
            'get by name':self.handle_get_name,
            'get by status':1,
            'get by id':1
        }
        command_functions[habit_field_number]()
        return True,'hello'
    

    @retry_until_success
    def filter(self):
        pass

    @retry_until_success
    def filter_by_name(self):
        pass

    @retry_until_success
    def filter_by_datetime(self):
        pass

    @retry_until_success
    def filter_by_duration(self):
        pass
