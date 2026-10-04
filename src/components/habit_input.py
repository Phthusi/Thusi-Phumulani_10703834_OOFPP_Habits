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
    """Manages form-based inputs, terminal interaction, and validation for habit objects.

    Handles setting, validating, and updating habit fields (name, start datetime,
    and session duration), detecting scheduling overlaps against saved habits, and
    persisting valid habits.

    Attributes:
        __habit (CompleteHabit): Habit instance being populated or edited.
        __datetime_manager (HabitDateTimeManager): Utility for processing datetimes and durations.
        __datetime_validator (HabitDateTimeManagerValidator): Validator for schedule formats and times.
        __BASE_DIR (Path): Root directory path for relative history file resolution.
        __view (View): View presenter interface.
        __shelf (Shelf): Local cache storage interface.
        __main_form (Form): Primary input form tracking field status flags and display layout.
    """
    def __init__(self, base_directory):
        """Initializes the input handler with required dependency configurations.

        Args:
            base_directory (Path): Base directory path for history resolution.
        """
        self.__start_setup(base_directory)

    def get_main_form(self):
        """Retrieves the primary main input form instance.

        Returns:
            Form: Form object managing status tracking of parameter fields.
        """
        return self.__main_form
    
    def __start_setup(self,base_directory):
        """Resets internal state variables and builds initial parameter tracking forms.

        Args:
            base_directory (Path): Base directory path for storage and history context.
        """
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
        """Exposes setup initialization to re-bind directory configurations.

        Args:
            base_directory (Path): Base directory path to configure.
        """
        self.__start_setup(base_directory)

    def __set_habit_name(self,message,field_pair=None, update_mode=False):
        """Prompts for habit name entry using history autocompletion.

        Args:
            message (str): Prompt display message.
            field_pair (tuple[bool, Any], optional): Field state tuple for autocompleter context. Defaults to None.
            update_mode (bool, optional): Whether command is operating in update mode. Defaults to False.

        Returns:
            str: Lowercase string entry from the user prompt.
        """
        history_file_name='habit_name'
        commands = []
        if update_mode:
            commands = ['reset name']
        self.__main_autocompleter = AutoCompleter(self.__BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/AddHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Text length minimum : 3 \nExample : Run\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()
    
    @retry_until_success
    def set_habit_name(self,message,form=None,name=None,field_value= None, update_mode=False):
        """Prompts, validates, and updates the active habit name field.

        Args:
            message (str): Terminal display prompt for name input.
            form (Form, optional): Reference target form. Defaults to primary form if None.
            name (str, optional): Default existing habit name text. Defaults to None.
            field_value (Any, optional): Current active value of field. Defaults to None.
            update_mode (bool, optional): Flag activating reset command capabilities. Defaults to False.

        Returns:
            tuple[bool, str]: Success flag and processing result message.
        """
        clear_screen()
        if form is None:
            form = self.__main_form

        if name is None:
            name = self.__habit.get_name()

        habit_name = self.__set_habit_name(message,(form.get_field_status('name',field_value= field_value, update_mode=update_mode),name), update_mode=update_mode)
        if update_mode and habit_name=='reset name':
            self.__habit.clear_name()
            self.__main_form.set_field_status('name',False)
            return True, 'success...'
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(habit_name)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        is_name_valid, message = self.__habit.set_name(habit_name)
        if is_name_valid:
            self.__main_form.set_field_status('name',True)
        return is_name_valid, message

    def __set_habit_start_datetime(self,message,field_pair=None,update_mode=False):
        """Prompts for start datetime input via autocompleted terminal prompt.

        Args:
            message (str): Terminal prompt string displayed to user.
            field_pair (tuple[bool, Any], optional): Status field tuple. Defaults to None.
            update_mode (bool, optional): Flag indicating if update reset commands apply. Defaults to False.

        Returns:
            str: Lowercase datetime input string.
        """
        history_file_name='start_datetime'
        commands = []
        if update_mode:
            commands = ['reset start_datetime']
        self.__main_autocompleter = AutoCompleter(self.__BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/AddHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Input Format  : YYYY-MM-DD HH:MM\nInput Example : 2026-06-30 16:45\nyear = 2026, month = June, day = 30th, time= 4pm, 45 minutes\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()

    def get_habit(self):
        """Retrieves the active habit model instance.

        Returns:
            CompleteHabit: Active habit instance being built or modified.
        """
        return self.__habit

    @retry_until_success
    def set_start_datetime(self,message,form=None,start_datetime=None,field_value= None, update_mode=False):
        """Prompts for, validates, and parses start datetime values onto the habit object.

        Args:
            message (str): Prompt text presented to user.
            form (Form, optional): Form to update field readiness status on. Defaults to None.
            start_datetime (str, optional): Existing start datetime string. Defaults to None.
            field_value (Any, optional): Active input value for form mapping. Defaults to None.
            update_mode (bool, optional): Enables value resetting commands when True. Defaults to False.

        Returns:
            tuple[bool, str]: Success flag and associated feedback text.
        """
        clear_screen()
        if form is None:
            form = self.__main_form

        if start_datetime is None:
            start_datetime = self.__habit.get_start_date()

        habit_start_datetime = self.__set_habit_start_datetime(message,(form.get_field_status('start_datetime',field_value=field_value,update_mode=update_mode),start_datetime),update_mode=update_mode).replace(',','')
        if update_mode and habit_start_datetime=='reset start_datetime':
            self.__habit.clear_start_date()
            self.__main_form.set_field_status('start_datetime',False)
            return True, 'success...'

        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_start_datetime)
        if did_run_common_func==False:
            return True, 'Escaping...'
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
        if not self.__datetime_validator.is_datetime_valid(habit_start_datetime):
            return False, 'Invalid format'
        
        if not self.__datetime_validator.is_passed(habit_start_datetime):
            return False, 'You cannot schedule for the time that has passed'

        self.__habit.set_start_date(self.__datetime_manager.string_to_datetime(habit_start_datetime))
        self.__main_form.set_field_status('start_datetime',True)
        return True, 'valid start datetime'

    def __set_habit_session_duration(self,message,example=None,field_pair=False, update_mode=False):
        """Prompts for habit duration entry using terminal input with history completion.

        Args:
            message (str): Prompt text displayed.
            example (str, optional): Unused formatting hint override. Defaults to None.
            field_pair (tuple[bool, Any], optional): Status-value pair tuple for history context. Defaults to False.
            update_mode (bool, optional): Whether update commands are permitted. Defaults to False.

        Returns:
            str: Lowercase user duration input.
        """
        history_file_name='session_duration'
        commands = []
        if update_mode:
            commands = ['reset duration']
        self.__main_autocompleter = AutoCompleter(self.__BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/AddHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Input Format  : HH:MM:SS\nInput Example : 01:17:20\nhours=1,minutes=17,seconds=20\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()
    
    def __set_habit(self,habit):
        """Binds a new CompleteHabit target instance internally.

        Args:
            habit (CompleteHabit): Habit instance to track.
        """
        self.__habit = habit

    @retry_until_success
    def set_session_duration(self,message,form=None,duration=None,field_value= None, update_mode=False):
        """Prompts, validates, and sets the session duration for the habit.

        Args:
            message (str): Terminal display prompt string.
            form (Form, optional): Form instance tracking status. Defaults to None.
            duration (str, optional): Default existing duration value. Defaults to None.
            field_value (Any, optional): Active value assigned in input form context. Defaults to None.
            update_mode (bool, optional): Allows reset duration command handling when True. Defaults to False.

        Returns:
            tuple[bool, str]: Success status and result status text.
        """
        clear_screen()
        if form is None:
            form = self.__main_form
        
        if duration is None:
            duration = self.__habit.get_session_duration()

        habit_session_duration = self.__set_habit_session_duration(message,field_pair=(form.get_field_status('duration',field_value= field_value, update_mode=update_mode),duration), update_mode=update_mode)
        if update_mode and habit_session_duration=='reset duration':
            self.__habit.clear_start_date()
            self.__main_form.set_field_status('duration',False)
            return True, 'success...'
        
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_session_duration)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************

        if not self.__datetime_validator.is_time_format_valid(habit_session_duration):
            return False, 'Invalid format'
        
        self.__main_form.set_field_status('duration',True)
        self.__habit.set_session_duration(habit_session_duration)
        return True, 'valid start datetime'

    def is_clashing_with_any_habit(self):
        """Checks if the active habit overlaps in schedule with active habits in the database.

        Returns:
            tuple[bool, str]: Tuple containing success boolean (True if no clash) and 
            formatted string message describing outcome or conflict.
        """
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
        next_id = max((habit[0] for habit in habits), default=0) + 1
        self.__shelf.preserve_habit((next_id,self.__habit.get_name(),self.__habit.get_start_date(),self.__habit.get_session_duration(),'UPCOMING',self.__habit.get_periodicity()))
        return True, f'✅ Habit saved successfully....\n{habit_to_be_added.replace("Habit to be added","Habit added")}'

    def get_clashing_habits(self,habits_to_be_added):
        """Identifies schedule overlap pairs between prospective and saved habits.

        Args:
            habits_to_be_added (list[tuple]): List of habit tuple definitions to test for schedule conflicts.

        Returns:
            list[tuple[tuple, tuple]]: Pairs of conflicting habit tuples in `(new_habit, saved_habit)` format.
        """
        habits = Habits().get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])
        clash_pairs = []
        for habit_to_be_added in habits_to_be_added:
            id_1, name_1, start_datetime_1, duration_1, status_1, periodicity_1 = habit_to_be_added
            for habit in habits:
                id, name, start_datetime, duration, status, periodicity = habit
                datetime2 = self.__datetime_manager.string_to_datetime(start_datetime)
                duration2 = self.__datetime_manager.convert_duration(duration)
                if self.__datetime_manager.is_clashing(self.__datetime_manager.string_to_datetime(start_datetime_1), self.__datetime_manager.convert_duration(duration_1), datetime2, duration2):
                    clash_pairs.append((habit_to_be_added, habit))
        return clash_pairs

    def save(self):
        """Validates, checks for scheduling conflicts, and persists active habit data.

        Returns:
            tuple[bool, str]: Tuple containing overall success indicator and status message.
        """
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

    def display_habit_pairs(self,habit_pairs):
        """Prints side-by-side terminal comparison views for conflicting pairs of habits.

        Args:
            habit_pairs (list[tuple[tuple, tuple]]): Collection of conflicting `(new_habit, db_habit)` pairs.
        """
        for count,habit_pair in enumerate(habit_pairs):
            habit_to_be_added, habit_from_db = habit_pair
            id_1, name_1, start_datetime_1, duration_1, status_1, periodicity_1 = habit_to_be_added
            id_2, name_2, start_datetime_2, duration_2, status_2, periodicity_2 = habit_from_db
            print(f'''CASE No:{count+1}
{Back.BLUE}{Fore.WHITE}            New Habit                    {Back.RESET}         {Back.BLUE}{Fore.WHITE}             Habit                       {Back.RESET}         
 id               : {id_2}                             id               : {id_1}
 name             :{name_2}                 CLASHES  name             :{name_1}
 start_datetime   :{start_datetime_2}     WITH    start_datetime   :{start_datetime_1}
 session_duration :{duration_2}                        session_duration :{duration_1}
 status           :{status_2}                        status           :{status_1}
 periodicity      :{periodicity_2}                            periodicity      :{periodicity_1}
 weekday          :{self.__datetime_manager.get_weekday(str(start_datetime_2).split(' ')[0])}                             weekday          :{self.__datetime_manager.get_weekday(str(start_datetime_2).split(' ')[0])}
-----------------------------------------         -----------------------------------------
''')