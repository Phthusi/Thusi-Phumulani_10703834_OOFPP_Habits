from ..data.db_manager import CompleteHabit, Habits
from .ui.command_autocomplete import AutoCompleter,Form
from .time_project.time_manager import HabitDateTimeManager
from .time_project.time_manager_validator import HabitDateTimeManagerValidator
from .ui.terminal_utils import ran_common_functions, retry_until_success
from .shelf import Shelf
from .view import View
from .ui.terminal_utils import clear_screen
from colorama import Fore, Style, Back

class Habit_Inputs:
    def __init__(self, base_directory):
        self.__start_setup(base_directory)

    def get_main_form(self):
        return self.__main_form
    
    def __start_setup(self,base_directory):
        self.__habit = CompleteHabit()
        self.__datetime_manager = HabitDateTimeManager()
        self.__datetime_validator = HabitDateTimeManagerValidator()
        self.__BASE_DIR = base_directory
        self.__view = View()
        self.__shelf = Shelf()
        display_map = """
[bold cyan]📌 LEVEL 1: PARAMETERS[/] [green]{name}[/] Name [bold blue] {start_datetime}[/] Start Datetime [green] {duration}[/] Duration  |  [bold cyan]🔒 LEVEL 2: ACTION(S) [/] Save"""
        self.__main_form = Form({field: False for field in ['name','start_datetime','duration']},display_map)

    def start_setup(self,base_directory):
        self.__start_setup(base_directory)

    def __set_habit_name(self,message,field_pair=None):
        history_file_name='habit_name'
        commands = []
        self.__main_autocompleter = AutoCompleter(self.__BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/AddHabit/{modified_history_file_name}",field_pair=field_pair,example=f'{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()
    
    @retry_until_success
    def set_habit_name(self,message):
        clear_screen()
        habit_name = self.__set_habit_name(message,(self.__main_form.get_field_status('name'),self.__habit.get_name()))
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(habit_name)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        is_name_valid, message = self.__habit.set_name(habit_name)
        if is_name_valid:
            self.__main_form.set_field_status('name',True)
        return is_name_valid, message

    def __set_habit_start_datetime(self,message,field_pair=None):
        history_file_name='start_datetime'
        commands = []
        self.__main_autocompleter = AutoCompleter(self.__BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/AddHabit/{modified_history_file_name}",field_pair=field_pair,example=f'{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()

    def get_habit(self):
        return self.__habit

    @retry_until_success
    def set_start_datetime(self,message):
        clear_screen()
        habit_start_datetime = self.__set_habit_start_datetime(message,(self.__main_form.get_field_status('start_datetime'),self.__habit.get_start_date())).replace(',','')

        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_start_datetime)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        try:
            date, time = habit_start_datetime.split(' ')
        except Exception:
            return False, 'Invalid format'
        
        if not (isinstance(date,str) and isinstance(date,str)):
            return False, 'Invalid format'

        time_list = time.split(':')
        if len(time_list)!=2:
            return False, 'Invalid format: time is not in a valid format'

        habit_start_datetime +=":00"
        if not self.__datetime_validator.is_date_valid(habit_start_datetime):
            return False, 'Invalid format'
        
        if not self.__datetime_validator.is_passed(habit_start_datetime):
            return False, 'You cannot schedule for the time that has passed'

        self.__habit.set_start_date(self.__datetime_manager.string_to_datetime(habit_start_datetime))
        self.__main_form.set_field_status('start_datetime',True)
        return True, 'valid start datetime'

    def __set_habit_session_duration(self,message,example=None,field_pair=False):
        history_file_name='session_duration'
        commands = []
        self.__main_autocompleter = AutoCompleter(self.__BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/AddHabit/{modified_history_file_name}",field_pair=field_pair,example=f'{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()
    
    def __set_habit(self,habit):
        self.__habit = habit

    @retry_until_success
    def set_session_duration(self,message):
        clear_screen()
        habit_session_duration = self.__set_habit_session_duration(message,field_pair=(self.__main_form.get_field_status('duration'),self.__habit.get_session_duration()))

        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_session_duration)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************

        if not self.__datetime_validator.is_time_format_valid(habit_session_duration):
            return False, 'Invalid format'
        
        self.__main_form.set_field_status('duration',True)
        self.__habit.set_session_duration(habit_session_duration)
        return True, 'valid start datetime'

    def is_clashing_with_any_habit(self):
        habits = Habits().get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])
        datetime1 = self.__habit.get_start_date()
        duration1 = self.__datetime_manager.convert_duration(self.__habit.get_session_duration())
        habit_to_be_added = f'''{Fore.WHITE}
{Back.BLUE}{Fore.WHITE}       Habit to be added                 {Back.RESET}
 id               :{self.__habit.get_id()}
 name             :{self.__habit.get_name()}
 start_datetime   :{datetime1}
 session_duration :{self.__habit.get_session_duration()}
 status           :N/A
 periodicity      :{self.__habit.get_periodicity()}
-----------------------------------------
'''
        for habit in habits: 
            id, name, start_datetime, duration, status, periodicity = habit
            datetime2 = self.__datetime_manager.string_to_datetime(start_datetime)
            duration2 = self.__datetime_manager.convert_duration(duration)
            if self.__datetime_manager.is_clashing(datetime1,duration1,datetime2,duration2):
                clear_screen()
                habit_from_db = f'''

{Back.BLUE}{Fore.WHITE}       Saved Habit                      {Back.RESET}
 id               : {id}
 name             :{name} 
 start_datetime   :{datetime2}
 session_duration :{duration}
 status           :{status}
 periodicity      :{self.__habit.get_periodicity()}
-----------------------------------------
'''
                return False, f'❌ Sorry Habit not saved, The following Habits are Clashing: \n{habit_to_be_added} \nAND {habit_from_db}'
        clear_screen()
        self.__shelf.preserve_habit((id+1,self.__habit.get_name(),self.__habit.get_start_date(),self.__habit.get_session_duration(),'UPCOMING',self.__habit.get_periodicity()))
        return True, f'✅ Habit saved successfully....\n{habit_to_be_added.replace("Habit to be added","Habit added")}'

    def save(self):
        is_valid, message = self._Habit_Inputs__habit._CompleteHabit__validator.validate()
        if not is_valid: return False, message
        success, message = self.is_clashing_with_any_habit()
        print(message)
        if is_valid and success:
            input(f'[{Fore.YELLOW}Please note that the habit is shared so that you can go straight to editing/repeating(if you want to) it without searching{Fore.RESET}]\n       [Press Enter to continue]     ')
            is_valid_habit,id = self.__habit.save_habit()
            self.__shelf.preserve_habit((id,self.__habit.get_name(),self.__habit.get_start_date(),self.__habit.get_session_duration(),self.__habit.get_status(),self.__habit.get_periodicity()))
            self.__start_setup(self.__BASE_DIR)
            return is_valid_habit, 'successfully saved'
        input('        [Press Enter to continue]       ')
        return False, 'Unsuccessful'
