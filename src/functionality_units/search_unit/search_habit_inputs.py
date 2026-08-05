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

    def __my_input(self,message,history_file_name,commands,field_pair=None,base='Home/SearchHabit/',example=None):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"{base}{modified_history_file_name}",field_pair=field_pair,example=example).lower()

    def get_main_form(self):
        return self.__main_form

    def display_copied_habit(self):
        self.__habit = Shelf.copy_last_place_habit() 
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state()}')

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
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Status/',search_input=f'status is {user_input}')
        return True,'success...'

    @retry_until_success
    def handle_get_habits_to_complete(self):
        results = self.__habit_search.get_habit_by_status('TO_BE_CONFIRMED')
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Status/HabitsToUpdate/',search_input=f'habits to complete')
        input('press any key to continue')
        return True,'success...'

    @retry_until_success
    def __get_habits_before(self):
        commands =  []
        history_file_name = 'before'
        user_input = self.__my_input('Enter time: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/',example='Input Example: 15:00:00')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_before_time(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Time/Before/',search_input=f'time before, {user_input}')
        return True,'success...'

    @retry_until_success
    def __get_habits_name_has(self):
        commands =  []
        history_file_name = 'has'
        user_input = self.__my_input('Enter name: ',history_file_name,commands,base='Home/SearchHabit/Filter/Name/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_by_has_name(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Name/Has/',search_input=f'has the following name \'{user_input}\'')
        return True,'success...'

    @retry_until_success
    def __get_by_duration_less_than(self):
        commands =  []
        history_file_name = 'less_than'
        user_input = self.__my_input('Enter duration: ',history_file_name,commands,base='Home/SearchHabit/Filter/Duration/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_by_duration_less_than(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Duration/LessThan/',search_input=f'duration less than, {user_input}')
        return True,'success...'

    @retry_until_success
    def __get_by_duration_greater_than(self):
        commands =  []
        history_file_name = 'greater_than'
        user_input = self.__my_input('Enter duration: ',history_file_name,commands,base='Home/SearchHabit/Filter/Duration/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_by_duration_greater_than(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Duration/GreaterThan/',search_input=f'duration greater than, {user_input}')
        return True,'success...'

    @retry_until_success
    def __get_by_duration(self):
        commands =  []
        history_file_name = 'at'
        user_input = self.__my_input('Enter duration: ',history_file_name,commands,base='Home/SearchHabit/Filter/Duration/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_by_duration(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Duration/At/',search_input=f'duration exactly equal to {user_input}')
        return True,'success...'

    @retry_until_success
    def __get_habits_before_date(self):
        commands =  []
        history_file_name = 'before'
        user_input = self.__my_input('Enter Date: ',history_file_name,commands,base='Home/SearchHabit/Filter/Date/',example='Input Example: 2026-06-30')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_before_date(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Date/Before/',search_input=f'Date Before {user_input}')
        return True,'success...'

    @retry_until_success
    def __get_habits_after(self):
        commands =  []
        history_file_name = 'after'
        user_input = self.__my_input('Enter time: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/',example='Input Example: 20:00:00')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_after_time(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Time/After/',search_input=f'time after, {user_input}')
        return True,'success...'
        
    @retry_until_success
    def __get_habits_name_is(self):
        commands =  []
        history_file_name = 'is'
        user_input = self.__my_input('Enter Name: ',history_file_name,commands,base='Home/SearchHabit/Filter/Name/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_by_name(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Name/Is/',search_input=f'name is \'{user_input}\'')
        return True,'success...'
    
    @retry_until_success
    def __get_habits_at(self):
        commands =  []
        history_file_name = 'on'
        user_input = self.__my_input('Select a time filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/',example='14:00:00')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_exactly_at(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Time/On/',search_input=f'time exactly at, {user_input}')
        return True,'success...'

    @retry_until_success
    def __get_habits_at_date(self):
        commands =  []
        history_file_name = 'on'
        user_input = self.__my_input('Select a Date filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Date/',example='Input Example: 2026-06-30')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_exactly_at_date(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Date/On/',search_input=f'date exactly is {user_input}')
        return True,'success...'
    
    @retry_until_success
    def __get_habits_after_date(self):
        commands =  []
        history_file_name = 'after'
        user_input = self.__my_input('Select a Date filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Date/',example='Input Example: 2026-06-30')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        results = self.__habit_search.get_habit_after_date(user_input)
        self.__view.display_habits(results,'Home/SearchHabit/Filter/Date/After/',search_input=f'Date After {user_input}')
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
            case default:
                return False,f'\'{user_input}\' is an valid input'

        return True,'hello'

    @retry_until_success
    def handle_get_duration(self):
        commands = ['less than','greater than','on']
        history_file_name = 'duration'
        user_input = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands,base='Home/SearchHabit/Filter/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        match user_input:
            case 'less than':
                self.__get_by_duration_less_than()
            case 'greater than':
                self.__get_by_duration_greater_than()
            case 'on':
                self.__get_by_duration()
            case default:
                return False,f'\'{user_input}\' is an valid input'

        return True,'hello'
    
    @retry_until_success
    def handle_get_date(self):
        commands = ['before','after','on']
        history_file_name = 'date'
        user_input = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands,base='Home/SearchHabit/Filter/')
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
                self.__get_habits_before_date()
            case 'after':
                self.__get_habits_after_date()
            case 'on':
                self.__get_habits_at_date()
            case default:
                return False,f'\'{user_input}\' is an valid input'

        return True,'hello'
    
    @retry_until_success
    def handle_get_name(self):
        commands = ['is','has']
        history_file_name = 'name'
        user_input = self.__my_input('Choose how you choose to find the habit(s): ',history_file_name,commands,base='Home/SearchHabit/Filter/')
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        match user_input:
            case 'is':
                self.__get_habits_name_is()
            case 'has':
                self.__get_habits_name_has()
            case default:
                return False,f'\'{user_input}\' is an valid input'

        return True,'hello'

    @retry_until_success
    def find_habits(self):
        commands = ['date','time','duration','name','status','habit to complete']
        history_file_name = 'filter'
        user_input = self.__my_input('How would you like to search for habits: ',history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
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
            'habit to complete': self.handle_get_habits_to_complete
        }
        if user_input in command_functions.keys():
            command_functions[user_input]()
        else:
            return False, f"'{user_input}' is an invalid input"
        
        return False,'hello'
    
    @retry_until_success
    def view_selected_habit(self):
        habit = Shelf.copy_last_place_habit()
        if habit is None:
            return True,'No habit has been selected'

        self.__view.draw_plain_table(habit)
        return True,'success...'
