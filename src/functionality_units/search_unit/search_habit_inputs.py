from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message
from ...data.db_manager import CompleteHabit, Habits
from ..habit_input import Habit_Inputs 
from colorama import Fore
from ..shelf import Shelf
from ..view import View


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# view after finding results -> decide stacking queries ->
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
        self.__saved_results = dict()
        self.__view = View()

    def __my_input(self,message,history_file_name,commands,field_pair=None,base='Home/SearchHabit/'):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"{base}{modified_history_file_name}",field_pair=field_pair).lower()

    def get_main_form(self):
        return self.__main_form

    def display_grabbed_habit(self):
        self.__habit = Shelf.copy_last_place_habit() 
        if self.__habit==None:
            print(f'''{Fore.LIGHTBLACK_EX}Status          : ❌ {self.__searched_habits_status}
Shared Habit ID : {Fore.LIGHTBLUE_EX}N/A''')
            return
        print(f'''{Fore.LIGHTBLACK_EX}Status          : ✅ {self.__searched_habits_status}
Shared Habit ID : {Fore.LIGHTGREEN_EX}{self.__habit[0]}''')

    @retry_until_success
    def handle_get_status(self):
        commands = ['MISSED','ONGOING','UPCOMING']
        history_file_name = 'status'
        user_input = self.__my_input('Enter habit status: ',history_file_name,commands,base='Home/SearchHabit/Filter/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************

        user_input = user_input.upper()
        if user_input not in commands:
            return False,f'\'{user_input}\' is not a valid status'
        
        results = self.__habit_search.get_habit_by_status(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Status/')
        return True,'success...'
    
    @retry_until_success
    def handle_get_id(self):
        commands = []
        history_file_name = 'id'
        habit_field_number = self.__my_input('Enter habit ID: ',history_file_name,commands,base='Home/SearchHabit/Filter/')
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
    def __get_habits_before(self):
        commands =  []
        history_file_name = 'before'
        user_input = self.__my_input('Enter time: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************

        results = self.__habit_search.get_habit_before_time(user_input)
        results = [
    (1, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (2, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (3, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (4, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (5, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (6, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (7, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (8, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (9, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (10, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (11, 'studying all day', '2026-06-01 14:10:00', '00:15:00', 'UPCOMING'), 
    (12, 'jogging', '2026-06-10 14:10:00', '00:15:00', 'UPCOMING'), 
    (13, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (14, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (15, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (16, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (17, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (18, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (19, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (20, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (21, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (22, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (23, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (24, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (25, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (26, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    ]
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Before/')
        return True,'success...'

    @retry_until_success
    def __get_habits_after(self):
        commands =  ['before','after','on']
        history_file_name = 'after'
        user_input = self.__my_input('Enter time: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_after_time(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/After/')
        return True,'success...'
        
    @retry_until_success
    def __get_habits_at(self):
        commands =  ['before','after','on']
        history_file_name = 'at'
        user_input = self.__my_input('Select a time filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_exactly_at(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/At/')
        return True,'success...'

    
    @retry_until_success
    def handle_get_time(self):
        commands =  ['before','after','on']
        history_file_name = 'time'
        user_input = self.__my_input('Select a time filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        if user_input not in commands:
            return False, f'\'{user_input}\' is not a valid input'
        
        match user_input:
            case 'before':
                self.__get_habits_before()
            case 'after':
                self.__get_habits_after()
            case 'on':
                self.__get_habits_at()
        return True,'hello'

    @retry_until_success
    def handle_get_duration(self):
        commands = ['less than','more than','equal to']
        history_file_name = 'duration'
        habit_field_number = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands,base='Home/SearchHabit/Filter/')
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
    def handle_get_date(self):
        commands = ['before','after','on']
        history_file_name = 'date'
        habit_field_number = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands,base='Home/SearchHabit/Filter/')
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
        commands = ['is','has']
        history_file_name = 'name'
        habit_field_number = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands,base='Home/SearchHabit/Filter/')
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
    def find_habits(self):
        data_source,success = self.__choose_data_source()
        if 'clearing screen'==success:
            return False,success
        if success=='escaping':
            return True,success
        if not success:
            return success, f'\'{data_source}\' does not exits'
    
        commands = ['date','time','duration','name','status','id']
        history_file_name = 'filter'
        habit_field_number = self.__my_input('How would you like to search for habits: ',history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        command_functions = {
            'date':self.handle_get_date,
            'time':self.handle_get_time,
            'duration':self.handle_get_duration,
            'name':self.handle_get_name,
            'status':self.handle_get_status,
            'id':self.handle_get_id
        }
        command_functions[habit_field_number]()
        
        # self.__save_results()
        return False,'hello'
    
    def __choose_data_source(self):
        commands = [i for i in self.__saved_results.keys() if i!='']
        commands.append('database')
        print(f'Selected Habit: {'N\A'} ')
        data_source = self.__my_input(
            'Where do you want to search from: ',
            'data_source',
            commands,
            base='Home/SearchHabit/'
        )
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(data_source)
        message_to_display = find_message(data_source)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        if data_source not in commands:
            return data_source, False
        return data_source, True

    @retry_until_success
    def __save_results(self):
        pass