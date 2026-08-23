from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message,clear_screen
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
        clear_screen()
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
        input('Press enter to continue')
        return True,'success...'

    @retry_until_success
    def __get_habits_before(self):
        commands =  []
        history_file_name = 'before'
        clear_screen()
        user_input = self.__my_input('Enter time: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/',example='Input Format  : HH:MM:SS\nInput Example : 15:30:45\nHours = 15, Minutes = 30, Seconds = 45'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
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
        clear_screen()
        user_input = self.__my_input('Enter duration: ',history_file_name,commands,base='Home/SearchHabit/Filter/Duration/',example='Input Format  : HH:MM:SS\nInput Example : 01:15:40\nHours = 1, Minutes = 15, seconds = 40'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
        user_input = self.__my_input('Enter duration: ',history_file_name,commands,base='Home/SearchHabit/Filter/Duration/',example='Input Format  : HH:MM:SS\nInput Example : 05:37:48\nHours = 5, Minutes = 37, seconds = 48'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
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
        clear_screen()
        user_input = self.__my_input('Enter Date: ',history_file_name,commands,base='Home/SearchHabit/Filter/Date/',example='Input Format  : YYYY-MM-DD\nInput Example : 2026-06-30\nyear = 2026, month = June, day = 30th'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
        user_input = self.__my_input('Enter time: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/',example='Input Format  : HH:MM:SS\nInput Example : 20:18:50\nHours = 20, Minutes = 18, Seconds=50'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
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
        clear_screen()
        user_input = self.__my_input('Select the time filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Time/',example='Input Format  : HH:MM:SS\nInput Example : 04:15:09\nHours = 4, Minutes = 15, Seconds=9'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
        user_input = self.__my_input('Select the Date filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Date/',example='Input Format  : YYYY-MM-DD\nInput Example : 2026-06-30\nyear = 2026, month = June, day = 30th'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
        clear_screen()
        user_input = self.__my_input('Select the Date filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/Date/',example='Input Format  : YYYY-MM-DD\nInput Example : 2026-06-30\nyear = 2026, month = June, day = 30th'+f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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

    def handle_get_time(self):
        history_file_name = 'time'
        command_functions = {
            'before':self.__get_habits_before,
            'after':self.__get_habits_after,
            'on':self.__get_habits_at,
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            user_input = self.__my_input('Select the time filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/',example=f'NB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            elif user_input in commands:
                funct = command_functions[user_input]
                funct()

            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
                input('Press enter to continue')

    def handle_get_duration(self):
        history_file_name = 'duration'
        command_functions = {
            'less than':self.__get_by_duration_less_than,
            'greater than':self.__get_by_duration_greater_than,
            'on':self.__get_by_duration,
        }
        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            user_input = self.__my_input('Select the Duration Filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/',example=f'\n{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            elif user_input in commands:
                funct = command_functions[user_input]
                funct()
            
            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
                input('Press enter to continue')

    def handle_get_date(self):
        history_file_name = 'date'
        command_functions = {
            'before':self.__get_habits_before_date,
            'after':self.__get_habits_after_date,
            'on':self.__get_habits_at_date,
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            user_input = self.__my_input('Select the Date Filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/',example=f'NB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            elif user_input in commands:
                funct = command_functions[user_input]
                funct()
            
            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
                input('Press enter to continue')

    def handle_get_name(self):
        history_file_name = 'name'
        command_functions = {
            'is':self.__get_habits_name_is,
            'has':self.__get_habits_name_has
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            user_input = self.__my_input('Select the Name Filter: ',history_file_name,commands,base='Home/SearchHabit/Filter/',example=f'NB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            elif user_input in commands:
                funct = command_functions[user_input]
                funct()
            
            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
                input('Press enter to continue')

    def find_habits(self):
        history_file_name = 'filter'
        command_functions = {
            'date':self.handle_get_date,
            'time':self.handle_get_time,
            'duration':self.handle_get_duration,
            'name':self.handle_get_name,
            'status':self.handle_get_status,
            'habit to complete': self.handle_get_habits_to_complete
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            user_input = self.__my_input('How would you like to search for habits: ',history_file_name,commands,example=f'\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            elif user_input in commands:
                funct = command_functions[user_input] 
                funct()
            
            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
                input('Press enter to continue')
    
    def view_selected_habit(self):
        habit = Shelf.copy_last_place_habit()
        if habit is None:
            print('No habit has been selected')
            input('Press enter to continue')
            return
        self.__view.draw_plain_table(habit)
        print('success...')
        input('Press enter to continue')
