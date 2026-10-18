from .habit_repeats_models import WeekPatternManager,WeekPattern,MonthPatternManager,MonthPattern, MonthsPattern
from .habit_repeats_validator import WeekPatternValidator,MonthPatternValidator, MonthsPatternValidator
from secrets import token_urlsafe
from ..habit_input import Habit_Inputs
from pathlib import Path
from ...data.db_manager import CompleteHabit
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.command_autocomplete import ProgressBar
from ..ui.terminal_utils import ran_common_functions, retry_until_success
from ..update_habit.update_habit_inputs import UpdateHabitInputs
from ..shelf import Shelf
from ...data.db_manager import Habits
from colorama import Fore, Style, Back
from ..time_project.time_manager import HabitDateTimeManager

BASE_DIR = Path(__file__).resolve().parent

class HabitRepeats:
    """Manages custom, daily, weekly, and monthly recurrence schedules for habit sessions.

    Coordinates terminal interactive forms, pattern aggregation (weeks, months, multi-month series),
    clash detection, and persistence into storage components (`Shelf` and database via `CompleteHabit`).

    Example:
        >>> repeater = HabitRepeats()
        >>> repeater.run_daily_repeats()
    """
    def __init__(self):
        """Initializes terminal UI forms, pattern managers, validators, shelf storage, and progress indicators."""
        self.__habit_inputs = Habit_Inputs(BASE_DIR)
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__week_pattern_manager = WeekPatternManager()
        self.__month_pattern_manager = MonthPatternManager()        
        self.__habits = Habits()
        self.__week_pattern = WeekPattern('default')
        self.__week_pattern_validator = WeekPatternValidator(self.__week_pattern)
        self.__month_pattern = MonthPattern('default')
        self.__month_pattern_validator = MonthPatternValidator(self.__week_pattern)
        self.__months_pattern = MonthsPattern()
        self.__months_pattern_validator = MonthsPatternValidator(self.__month_pattern)
        self.__shelf = Shelf()
        self.progress_bar = ProgressBar(7)
        self.__number_of_weeks = 0
        self.__number_of_days = 0
        self.__number_of_months = 0
        self.__habit_date_time_manger = HabitDateTimeManager()
        self.__levels = {'level1':'➡️','level2':' ','level3':' ','level4':' '}
        self.display_map = """
    ----------------------------------------------------------------------------------------------------------------------------
{level1}   [bold cyan]📌 LEVEL 1: PARAMETERS[/] [green]{week_pattern_name}[/] Week Pattern Name    {week_pattern} Week Pattern
    ----------------------------------------------------------------------------------------------------------------------------
{level2}   [bold cyan]📌 LEVEL 2: PARAMETERS[/] [green]{month_pattern_name}[/] Month Pattern Name   {month_pattern} Month Pattern
    ----------------------------------------------------------------------------------------------------------------------------
{level3}   [bold cyan]📌 LEVEL 3: PARAMETERS[/] [green]{months_pattern}[/] Months Pattern
    ---------------------------------------------------------------------------------------------------------------------------- 
{level4}    [bold cyan]🔒 LEVEL 4: ACTION(S) [/] Save"""
        self.__form = Form({field: False for field in ['week_pattern_name','week_pattern','month_pattern','month_pattern_name','months_pattern']},self.display_map,levels=self.__levels)
        self.__current_filled_fields = self.__form.number_of_filled_fields()

    def __my_input(self,message,history_file_name,commands,field_pair=None,example=None,multiple_values=''):
        """Internal helper to render auto-completion prompts, updating progress bar state on form changes.

        Args:
            message (str): Prompt text displayed to the user.
            history_file_name (str): History file path target inside the history directory.
            commands (list[str]): Available command strings for auto-completion.
            field_pair (tuple[str, str] | None): Tuple containing status and current string values.
            example (str | None): Guidance text or usage rules displayed above the prompt.
            multiple_values (str): Additional context string (e.g. current selected items list).

        Returns:
            str: Lowercased user input received from autocompleter prompt.
        """
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        if self.__current_filled_fields != self.__form.number_of_filled_fields():
            self.progress_bar.increase_progress_percentage(self.__form.number_of_filled_fields())
            self.__current_filled_fields = self.__form.number_of_filled_fields()
            self.__level_management(self.__current_filled_fields)

        self.progress_bar.display_progress_bar(self.__form.get_display_map())
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=example,multiple_values=multiple_values).lower()

    def __level_management(self,no_of_filled_fields):
        """Updates internal level indicator arrows based on filled parameter count.

        Args:
            no_of_filled_fields (int): Number of completed form fields.
        """
        match no_of_filled_fields:
            case 2:
                self.__levels = {'level1':' ','level2':'➡️','level3':' ','level4':' '}
            case 4:
                self.__levels = {'level1':' ','level2':' ','level3':'➡️','level4':' '}
            case 5:
                self.__levels = {'level1':' ','level2':' ','level3':' ','level4':'➡️'}

    def __set_habit_week_pattern_name(self,message,field_pair=None):
        """Prompts user for a unique week pattern identifier string.

        Args:
            message (str): Output prompt message.
            field_pair (tuple[str, str] | None): Status flag and currently assigned value.

        Returns:
            str: Lowercase string entry from prompt input.
        """
        history_file_name='week_pattern_name'
        commands = []
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'{'-'*95}\nRules\n{'-'*95}\n - Each month must have a unique name\n - Each week must have a unique name\n - The name must have the minimum of 3 characters\n - Name must only be a mixture of alphabet and numbers\n - Name must only start with alphabets\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()

    @retry_until_success
    def set_habit_week_pattern_name(self,message):
        """Handles setting and validating a new week pattern name.

        Args:
            message (str): Prompt text passed to terminal input handler.

        Returns:
            tuple[bool, str]: Status tuple containing:
                - bool: True if operation completed or escaped, False if switching.
                - str: Validation error or operational outcome text.

        Example:
            >>> repeater.set_habit_week_pattern_name("Enter week pattern name: ")
            (True, 'name is valid')
        """
        clear_screen()
        week_pattern_name = self.__set_habit_week_pattern_name(message,(self.__form.get_field_status('week_pattern_name'),self.__week_pattern.get_name()))
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(week_pattern_name)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        
        is_week_pattern_valid, message = self.__week_pattern_validator.is_name_pattern_valid(week_pattern_name, self.__week_pattern_manager.get_saved_weeks().keys())
        if is_week_pattern_valid:
            self.__form.set_field_status('week_pattern_name',True)
            self.__level_management(self.__form.number_of_filled_fields())
            self.__form = Form(self.__form.get_fields(),self.display_map,levels=self.__levels)
            self.__week_pattern.set_name(week_pattern_name)
        return is_week_pattern_valid, message

    def __set_habit_week_pattern(self,message,field_pair=None):
        """Prompts user for space-separated weekday tokens.

        Args:
            message (str): Output prompt message.
            field_pair (tuple[str, str] | None): Status flag and currently assigned name value.

        Returns:
            str: Lowercase space-separated weekday string.
        """
        history_file_name='week_pattern'
        commands = ['mon','tue','wed','thu','fri','sat','sun']
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        multiple_values = f"\nCurrent Value list : {Fore.LIGHTBLUE_EX if self.__week_pattern.week_patterns is None else Fore.LIGHTGREEN_EX}{self.__week_pattern.week_patterns if self.__week_pattern.week_patterns is not None else 'N/A'}{Fore.RESET}"
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Options\nmon, tue, wed, thu, fri, sat and sun\n{'-'*95}\nRules\n{'-'*95}\n - Enter Weekdays and separate them by a single space\n - Week days represent the days you choose per week, you must have at least one day\n - The order of putting the weekdays does not matter e.g mon tue fri wed is valid\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',multiple_values=multiple_values).lower()

    def reset(self):
        """Resets the internal state of the habit repeats manager, clearing all patterns and form fields."""
        self.__habit_inputs = Habit_Inputs(BASE_DIR)
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__week_pattern_manager = WeekPatternManager()
        self.__month_pattern_manager = MonthPatternManager()        
        self.__habits = Habits()
        self.__week_pattern = WeekPattern('default')
        self.__week_pattern_validator = WeekPatternValidator(self.__week_pattern)
        self.__month_pattern = MonthPattern('default')
        self.__month_pattern_validator = MonthPatternValidator(self.__week_pattern)
        self.__months_pattern = MonthsPattern()
        self.__months_pattern_validator = MonthsPatternValidator(self.__month_pattern)
        self.__shelf = Shelf()
        self.progress_bar = ProgressBar(7)
        self.__number_of_weeks = 0
        self.__number_of_days = 0
        self.__number_of_months = 0
        self.__habit_date_time_manger = HabitDateTimeManager()
        self.__levels = {'level1':'➡️','level2':' ','level3':' ','level4':' '}
        self.display_map = """
    ----------------------------------------------------------------------------------------------------------------------------
{level1}   [bold cyan]📌 LEVEL 1: PARAMETERS[/] [green]{week_pattern_name}[/] Week Pattern Name    {week_pattern} Week Pattern
    ----------------------------------------------------------------------------------------------------------------------------
{level2}   [bold cyan]📌 LEVEL 2: PARAMETERS[/] [green]{month_pattern_name}[/] Month Pattern Name   {month_pattern} Month Pattern
    ----------------------------------------------------------------------------------------------------------------------------
{level3}   [bold cyan]📌 LEVEL 3: PARAMETERS[/] [green]{months_pattern}[/] Months Pattern
    ---------------------------------------------------------------------------------------------------------------------------- 
{level4}    [bold cyan]🔒 LEVEL 4: ACTION(S) [/] Save"""
        self.__form = Form({field: False for field in ['week_pattern_name','week_pattern','month_pattern','month_pattern_name','months_pattern']},self.display_map,levels=self.__levels)
        self.__current_filled_fields = self.__form.number_of_filled_fields()

    @retry_until_success
    def set_habit_week_pattern(self,message):
        """Validates and persists weekday tokens associated with the current week pattern name.

        Args:
            message (str): Prompt text.

        Returns:
            tuple[bool, str]: Status tuple indicating success/failure and operational message.

        Example:
            >>> repeater.set_habit_week_pattern("Enter days: ")
            (True, 'week pattern saved successfully')
        """
        clear_screen()
        week_pattern = self.__set_habit_week_pattern(message,(self.__form.get_field_status('week_pattern'),None if self.__week_pattern.get_name()=='default' else self.__week_pattern.get_name()))
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(week_pattern)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        
        if self.__week_pattern.get_name()=='default':
            return False,'please set the week pattern name first'
        
        is_week_pattern_valid, message = self.__week_pattern_validator.is_week_pattern_valid(week_pattern.split(' '))
        if is_week_pattern_valid:
            self.__form.set_field_status('week_pattern',True)
            self.__level_management(self.__form.number_of_filled_fields())
            self.__form = Form(self.__form.get_fields(),self.display_map,levels=self.__levels)
            return self.__week_pattern_manager.save_week_pattern(self.__week_pattern.get_name(),week_pattern.split(' '))
        return is_week_pattern_valid, message

    def __set_habit_month_pattern(self,message,field_pair=None):
        """Prompts user to enter 4 registered week pattern names (or 'skip') for month composition.

        Args:
            message (str): Output prompt message.
            field_pair (tuple[str, str] | None): Status flag and currently assigned month pattern name.

        Returns:
            str: Lowercase string containing four space-separated week identifiers.
        """
        history_file_name='month_pattern'
        commands = self.__week_pattern.week_patterns.keys()
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        multiple_values = f"\nCurrent Value list : {Fore.LIGHTBLUE_EX if self.__month_pattern.monthPatterns is None else Fore.LIGHTGREEN_EX}{self.__month_pattern.monthPatterns if self.__month_pattern.monthPatterns is not None else 'N/A'}{Fore.RESET}"
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'{'-'*95}\nTips : Press space to see saved weeks\n{'-'*95}\nRules\n{'-'*95}\n - A month must have four weeks\n - Weeks must be chosen from saved weeks\n - The order of weeks matters\n - For the week you want to skip, just enter skip\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',multiple_values=multiple_values).lower()

    @retry_until_success
    def set_habit_month_pattern(self,message):
        """Validates and persists a 4-week month pattern under the current month pattern name.

        Args:
            message (str): Terminal prompt string.

        Returns:
            tuple[bool, str]: Outcome flag and validation string.

        Example:
            >>> repeater.set_habit_month_pattern("Enter 4 week patterns: ")
            (True, 'month pattern saved successfully')
        """
        clear_screen()
        if self.__week_pattern.week_patterns == {}:
            return True,'please set the week pattern first'
        
        month_pattern = self.__set_habit_month_pattern(message,(self.__form.get_field_status('month_pattern'),self.__month_pattern.get_name()))
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(month_pattern)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************

        if self.__month_pattern.get_name()=='default':
            return False,'please set the month pattern name first'
        
        is_month_pattern_valid, message = self.__month_pattern_validator.is_month_pattern_valid(month_pattern.split(' '))
        if is_month_pattern_valid:
            self.__form.set_field_status('month_pattern',True)
            self.__level_management(self.__form.number_of_filled_fields())
            self.__form = Form(self.__form.get_fields(),self.display_map,levels=self.__levels)
            return self.__month_pattern_manager.save_month_pattern(self.__month_pattern.get_name(),month_pattern.split(' '))
        return is_month_pattern_valid, message

    def __set_habit_month_pattern_name(self,message,field_pair=None):
        """Prompts user for a unique month pattern identifier string.

        Args:
            message (str): Prompt text.
            field_pair (tuple[str, str] | None): Status flag and currently assigned name.

        Returns:
            str: Lowercase string entry.
        """
        history_file_name='month_pattern_name'
        commands = []
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'{'-'*95}\nRules\n{'-'*95}\n - The name must have the minimum of 3 characters\n - Name must only be a mixture of alphabet and numbers\n - Name must only start with alphabets\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()

    @retry_until_success
    def set_habit_month_pattern_name(self,message):
        """Validates and assigns a new month pattern name.

        Args:
            message (str): Prompt text displayed to user.

        Returns:
            tuple[bool, str]: Validation tuple (success_boolean, feedback_message).

        Example:
            >>> repeater.set_habit_month_pattern_name("Enter month pattern name: ")
            (True, 'name is valid')
        """
        clear_screen()
        month_pattern_name = self.__set_habit_month_pattern_name(message,(self.__form.get_field_status('month_pattern_name'),self.__month_pattern.get_name()))
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(month_pattern_name)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        
        is_month_pattern_valid, message = self.__week_pattern_validator.is_name_pattern_valid(month_pattern_name, self.__month_pattern_manager.get_saved_months().keys())
        if is_month_pattern_valid:
            self.__form.set_field_status('month_pattern_name',True)
            self.__level_management(self.__form.number_of_filled_fields())
            self.__form = Form(self.__form.get_fields(),self.display_map,levels=self.__levels)
            self.__month_pattern.set_name(month_pattern_name)
        return is_month_pattern_valid, message

    def __set_habit_months_pattern(self,message,field_pair=None):
        """Prompts user to select an ordered list of saved month patterns (or 'skip').

        Args:
            message (str): Output prompt string.
            field_pair (tuple[str, str] | None): Status flag and currently active selection name.

        Returns:
            str: Lowercase string of space-delimited month identifiers.
        """
        history_file_name='months_pattern'
        commands = self.__month_pattern.monthPatterns.keys()

        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        multiple_values = f"\nCurrent Value list : {Fore.LIGHTBLUE_EX if self.__month_pattern.monthPatterns is None else Fore.LIGHTGREEN_EX}{self.__month_pattern.monthPatterns if self.__month_pattern.monthPatterns is not None else 'N/A'}{Fore.RESET}"
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',multiple_values=multiple_values).lower()

    @retry_until_success
    def set_habit_months_pattern(self,message):
        """Validates and persists the top-level multi-month schedule pattern.

        Args:
            message (str): Prompt text.

        Returns:
            tuple[bool, str]: Validation tuple (success_boolean, status_text).

        Example:
            >>> repeater.set_habit_months_pattern("Enter month patterns: ")
            (True, 'months pattern saved successfully')
        """
        clear_screen()
        months_pattern = self.__set_habit_months_pattern(message,(self.__form.get_field_status('months_pattern'),None if len(self.__month_pattern.get_month_pattern()) == 0 else self.__month_pattern.get_name()))
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(months_pattern)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************
        
        if self.__week_pattern.get_name()=='default':
            return False,'please set the week pattern name first'
        
        if self.__month_pattern.get_name()=='default':
            return False,'please set the month pattern name first'
        
        if len(self.__month_pattern.monthPatterns.keys())==0:
            return False,'please set the month pattern first'

        is_months_pattern_valid, message = self.__months_pattern_validator.is_months_pattern_valid(months_pattern.split(' '))
        if is_months_pattern_valid:
            self.__form.set_field_status('months_pattern',True)
            self.__level_management(self.__form.number_of_filled_fields())
            self.__form = Form(self.__form.get_fields(),self.display_map,levels=self.__levels)
            self.__months_pattern.set_months_pattern(months_pattern.split(' '))
            return self.__months_pattern.save_months_pattern()
        return is_months_pattern_valid, message

    def __save_habit_repeats(self,copied_habit,months_pattern=None):
        """Generates future habit occurrences from pattern structure, filters clashing schedules, and persists valid habits.

        Args:
            copied_habit (tuple): Base habit tuple (id, name, datetime_str, duration, status, periodicity).
            months_pattern (list[dict] | None): Custom months schedule structure, defaults to loaded `months_pattern`.
        """
        id, name, start_date , duration, status, periodicity = copied_habit
        copied_habit_id = id
        current_day,time = copied_habit[2].split(' ')
        habits_to_add = []
        
        if months_pattern is None:
            months_pattern = self.__months_pattern.get_months_pattern()
        
        current_day = self.__habit_date_time_manger.increase_by_day(current_day)

        for i in months_pattern:
            if list(i.keys())[0] == 'skip':
                for _ in range(7*4):
                    current_day = self.__habit_date_time_manger.increase_by_day(current_day)
                continue

            for j in i[list(i.keys())[0]]:
                if j == 'skip':
                    for _ in range(7):
                        current_day = self.__habit_date_time_manger.increase_by_day(current_day)
                    continue

                week_days = self.__week_pattern_manager.find_week_pattern(j)
                for _ in range(7):
                    if self.__habit_date_time_manger.get_weekday(current_day) in week_days:
                        habits_to_add.append((id, name, f'{current_day} {time}', duration, status, periodicity)) 
                    current_day = self.__habit_date_time_manger.increase_by_day(current_day)
       
        clash_pairs = self.__habit_inputs.get_clashing_habits(habits_to_add)
        if len(clash_pairs)!=0:
            first_part_of_the_pair = list(map(lambda pair:pair[0],clash_pairs))
            second_part_of_the_pair = list(map(lambda pair:pair[1],clash_pairs))
            self.__habit_inputs.display_habit_pairs(clash_pairs)
            habits_to_add = [habit for habit in habits_to_add if habit not in first_part_of_the_pair and habit not in second_part_of_the_pair]
            input('Press enter to continue')
        
        id = 0
        for habit in habits_to_add:
            id, name, start_date, session_duration, status, periodicity = habit
            success, id =CompleteHabit(name, session_duration, start_date, status,periodicity=periodicity).save_habit()
        
        copied_habit = self.__habits.get_habit_by_id(copied_habit_id)[0]
        updated_periodicity = periodicity

        if len(habits_to_add) > 0:
            self.__shelf.preserve_habit((id,name,start_date,session_duration,status,periodicity))

        id, name, start_date , duration, status, periodicity = copied_habit
        copied_habit_periodicity_is_null = periodicity is None
        if copied_habit_periodicity_is_null:
            CompleteHabit(name, duration, start_date, status,periodicity=copied_habit,id=copied_habit_id).update_habit(periodicity=updated_periodicity)
        self.reset()

    def save(self):
        """Saves custom habit repeating sessions based on active shelf copy and configured parameters.

        Returns:
            tuple[bool, str]: Success flag and completion message.

        Example:
            >>> repeater.save()
            (True, 'success...')
        """
        copied_habit = self.__shelf.copy_last_place_habit()
        id, name, start_datetime , duration, status, periodicity = copied_habit
        if status == 'MISSED':
            return False, 'sorry we cannot perform this operation for MISSED sessions'
        self.__save_habit_repeats((id, name, start_datetime , duration, status, 'CUSTOM'))
        return True,'success...'

    def run_custom_repeats(self):
        """Executes the interactive command menu loop for fully customized repeat schedule setup.

        Example:
            >>> repeater.run_custom_repeats()
        """
        command_functions = {
            'week pattern name':[
                    self.set_habit_week_pattern_name,
                    "Enter the week pattern name: "
                ],
            'week pattern':[
                self.set_habit_week_pattern,
                "Enter the week pattern: "
                ],
            'month pattern name':[
                    self.set_habit_month_pattern_name,
                    "Enter the month pattern name: "
                ],
            'month pattern':[
                    self.set_habit_month_pattern,
                    "Enter the month pattern: "
                    ],
            'months pattern':[
                 self.set_habit_months_pattern,
                 'Enter the months pattern: '
            ],
            'save':[
                self.save,
                ''
            ]
        }
        while True:
            clear_screen()
            if all(self.__form.fields.values()):
                self.__form.set_display_map(self.__form.get_raw_map().replace('🔒','🔓'))
            if not all(self.__form.fields.values()):
                self.__form.set_display_map(self.__form.get_raw_map().replace('🔓','🔒'))
            commands = list(command_functions.keys())
            history_file_name = 'custom_repeat_habit'
            user_input = self.__my_input("Enter command: ",history_file_name,commands,example='┌💁  Please note that you must start filling the level one parameters before you do the actions in level 2 ⸣\n⸤💡  [↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands         ⸥')
            
            match user_input:
                case 'esc':
                    break
                case 'clear':
                    clear_screen()
            
            if user_input not in commands:
                print('invalid input')
                continue
            
            func,message = command_functions[user_input]
            if message =='':
                success, message = func()
                if user_input == 'save' and message=='successfully saved':
                    self.progress_bar = ProgressBar(4)
                    self.__habit_inputs.start_setup(BASE_DIR)
                    self.__form = self.__habit_inputs.get_main_form()
                    self.__current_filled_fields = self.__form.number_of_filled_fields()
                    self.__form.set_display_map(self.__form.get_raw_map().replace('🔓','🔒'))
            else:
                display_message = func(message)

    @retry_until_success
    def set_number_of_pattern_entities(self,message,entity_name):
        """Sets numeric counts for repeating cycles (days, weeks, or months).

        Args:
            message (str): Output prompt string.
            entity_name (str): The entity count target ('days', 'weeks', or 'months').

        Returns:
            tuple[bool, str]: Validation outcome and confirmation message.

        Example:
            >>> repeater.set_number_of_pattern_entities("Enter weeks count: ", "weeks")
            (True, 'Number of weeks was set successfully...')
        """
        clear_screen()
        commands = []
        history_file_name = f'set_number_of_{entity_name}'

        match entity_name:
            case 'weeks':
                state_message = f'✅ Number of {entity_name} filled'if self.__number_of_weeks!=0 else f'❌ Number of {entity_name} not filled'
                current_value = self.__number_of_weeks if self.__number_of_weeks!=0 else f'{Fore.BLUE}N/A{Fore.RESET}'
            case 'months':
                state_message = f'✅ Number of {entity_name} filled'if self.__number_of_months!=0 else f'❌ Number of {entity_name} not filled'
                current_value = self.__number_of_months if self.__number_of_months!=0 else f'{Fore.BLUE}N/A{Fore.RESET}'
            case 'days':
                state_message = f'✅ Number of {entity_name} filled'if self.__number_of_days!=0 else f'❌ Number of {entity_name} not filled'
                current_value = self.__number_of_days if self.__number_of_days!=0 else f'{Fore.BLUE}N/A{Fore.RESET}'

        field_pair = (state_message,current_value)   

        user_input = self.__basic_input(f"Enter number of {entity_name}: ",commands,history_file_name,'[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',f'/{entity_name.title()}RepeatHabit/NumberOf{entity_name.title()}',field_pair=field_pair)
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(user_input)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'Switching...'
        # ********** end of common functions ************
        is_user_input_valid = user_input.isdigit()
        # self.save
        if not is_user_input_valid:
            return False, 'Invalid input. Please enter a number.'
        if int(user_input) == 0:
            return False, f'Invalid input. the number of {entity_name} must be greater than 0.'
        match entity_name:
            case 'days':
                self.__number_of_days = int(user_input)
                return True, f'Number of {entity_name} was set successfully...'
            case 'weeks':
                self.__number_of_weeks = int(user_input)
                return True, f'Number of {entity_name} was set successfully...'
            case 'months':
                self.__number_of_months = int(user_input)
                return True, f'Number of {entity_name} was set successfully...'
            case _:
                return True, f'Number of {entity_name} does not exist'

    @retry_until_success
    def save_week(self, *args,**kwargs):
        """Generates, validates, and saves weekly repeating habits across configured week iterations.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            tuple[bool, str]: Outcome flag and execution status text.

        Example:
            >>> repeater.save_week()
            (True, 'Success...')
        """
        if self.__number_of_weeks == 0:
            return True, 'Set the number of weeks first'

        if self.__week_pattern.get_name()=='default':
            return True, 'Set the week name first'

        if self.__week_pattern.week_patterns == {}:
            return True, 'Set the week pattern first'

        history_file_name = 'weekly_repeat_habit_name'
        user_input = self.__basic_input("Enter the name of the week you want to save(press enter to see your options): ",list(self.__week_pattern.week_patterns.keys()),history_file_name,f'\nPlease note that the week pattern you are choosing will be repeated {self.__number_of_weeks} times, because you chose to repeat this pattern\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',f'/WeeklyRepeatHabit/WeekPatternName')
        # ********* start of common functions ************
        did_run_common_func = ran_common_functions(user_input)
        if did_run_common_func==False:
            return True, 'Escaping...'
        elif did_run_common_func==True:
            return False, 'Switching...'
        # ********** end of common functions ************

        if not self.__week_pattern_validator.week_pattern_exists(user_input):
            return False, f'\'{user_input}\' does not exist'
       
        week_pattern_name = user_input
        added_months = []
        count = self.__number_of_weeks
        total_months_with_four_of_given_week = count // 4
        total_of_given_week_that_will_have_skips = count % 4
        
        for _ in range(total_months_with_four_of_given_week):
            month_name = f'month_id_{token_urlsafe(16)}'
            self.__month_pattern.set_name(month_name)
            added_months.append(month_name)
            self.__month_pattern_manager.save_month_pattern(month_name,[week_pattern_name,week_pattern_name,week_pattern_name,week_pattern_name])

        if total_of_given_week_that_will_have_skips!=0:        
            last_month_pattern = [week_pattern_name] * total_of_given_week_that_will_have_skips
            last_month_pattern.extend(['skip'] * (4 - total_of_given_week_that_will_have_skips))
            month_name = f'month_id_{token_urlsafe(16)}'
            self.__month_pattern.set_name(month_name)
            added_months.append(month_name)
            self.__month_pattern_manager.save_month_pattern(month_name,last_month_pattern)
        
        # save months pattern
        self.__months_pattern.set_months_pattern(added_months)
        self.__months_pattern.save_months_pattern()
        copied_habit = self.__shelf.copy_last_place_habit()
        # (1, 'studying', '2026-09-30 16:49:00', '00:25:00', 'UPCOMING', 'DAILY')
        copied_id,copied_name,copied_startdatetime,copied_duration,copied_status,copied_periodicity = copied_habit
        copied_habit = (copied_id,copied_name,copied_startdatetime,copied_duration,copied_status,'WEEKLY')
        filtered_months_pattern = [{list(i.keys())[0]: list(i.values())[0]} for i in self.__months_pattern.get_months_pattern()]

        self.__save_habit_repeats(copied_habit,months_pattern=filtered_months_pattern)
        print(f"Week data saved: {self.__number_of_weeks} weeks")
        return True, 'Success...'

    @retry_until_success
    def save_day(self, *args,**kwargs):
        """Generates, chunks into 7-day weeks, and persists daily repeating habit sessions.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            tuple[bool, str]: Success flag and completion status text.

        Example:
            >>> repeater.save_day()
            (True, 'Success...')
        """
        if self.__number_of_days == 0:
            return True, 'Set the number of days first'
 
        count = self.__number_of_days
        total_week_with_seven_days_of_given_week = count // 7
        days_left_to_complete_the_week           = count % 7
        number_of_skipped_days                   = 7 - days_left_to_complete_the_week
        number_weekdays_pairs = {
            1: ['mon'],
            2: ['mon', 'tue'],
            3: ['mon', 'tue', 'wed'],
            4: ['mon', 'tue', 'wed', 'thu'],
            5: ['mon', 'tue', 'wed', 'thu', 'fri'],
            6: ['mon', 'tue', 'wed', 'thu', 'fri', 'sat'],
        }
        added_weeks = []
        added_months = []

        for _ in range(total_week_with_seven_days_of_given_week):
            week_name = f'week_id_{token_urlsafe(16)}'
            self.__week_pattern.set_name(week_name)
            added_weeks.append(week_name)
            self.__week_pattern_manager.save_week_pattern(week_name,['mon','tue','wed','thu','fri','sat','sun'])

        if days_left_to_complete_the_week!=0:
            week_name = f'week_id_{token_urlsafe(16)}'
            self.__week_pattern.set_name(week_name)
            added_weeks.append(week_name)
            temporary_week_pattern = number_weekdays_pairs[days_left_to_complete_the_week]
            temporary_week_pattern.extend(['skip'] * number_of_skipped_days)
            self.__week_pattern_manager.save_week_pattern(week_name,temporary_week_pattern)

        for _ in range(total_week_with_seven_days_of_given_week if total_week_with_seven_days_of_given_week!=0 else 1):
            grouped_weeks = [added_weeks[i:i+4] for i in range(0, len(added_weeks), 4)]
            for week_group in grouped_weeks:
                month_name = f'month_id_{token_urlsafe(16)}'
                self.__month_pattern.set_name(month_name)
                added_months.append(month_name)
                if len(week_group) < 4:
                    week_group.extend(['skip'] * (4 - len(week_group)))
                self.__month_pattern_manager.save_month_pattern(month_name,week_group)
        
        # save months pattern
        self.__months_pattern.set_months_pattern(added_months)
        self.__months_pattern.save_months_pattern()
        copied_habit = self.__shelf.copy_last_place_habit()
        copied_id,copied_name,copied_startdatetime,copied_duration,copied_status,copied_periodicity = copied_habit
        copied_habit = (copied_id,copied_name,copied_startdatetime,copied_duration,copied_status,'DAILY')
        filtered_months_pattern = [{list(i.keys())[0]: list(i.values())[0]} for i in self.__months_pattern.get_months_pattern()]

        self.__save_habit_repeats(copied_habit,months_pattern=filtered_months_pattern)
        print(f"Day data saved: {self.__number_of_days} days")
        return True, 'Success...'

    def run_daily_repeats(self):
        """Runs the command loop for configuring simple daily repetition schedules."""
        command_functions = {
            'number of days':[
                lambda :self.set_number_of_pattern_entities(message='Enter the number days you want to repeat this habit session: ',entity_name='days'),
                ''
            ],
            'save':[
                self.save_day,
                ''
            ]
        }
        while True:
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'daily_repeat_habit'
            user_input = self.__basic_input("Enter command: ",commands,history_file_name,'[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands','/DailyRepeatHabit')            
            match user_input:
                case 'esc':
                    break
                case 'clear':
                    clear_screen()
            
            if user_input not in commands:
                print('invalid input')
                input('Press Enter to continue')
                continue
            
            func,message = command_functions[user_input]
            if message =='':
                success, message = func()
            else:
                display_message = func(message)

    def run_week_repeats(self):
        """Executes the interactive loop for configuring weekly repeat patterns.

        Presents sub-commands for pattern name, weekday selections, duration count,
        and final persistence execution.
        """
        command_functions = {
            'week pattern name':[
                    self.set_habit_week_pattern_name,
                    "Enter the week pattern name: "
                ],
            'week pattern':[
                self.set_habit_week_pattern,
                "Enter the week pattern: "
                ],
            'number of weeks':[
                self.set_number_of_pattern_entities,
                'Enter the number of weeks: '
            ],
            'save':[
                self.save_week,
                ''
            ]
        }
        while True:
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'weekly_repeat_habit'
            user_input = self.__basic_input("Enter command: ",commands,history_file_name,'[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands','/WeeklyRepeatHabit')            
            match user_input:
                case 'esc':
                    break
                case 'clear':
                    clear_screen()
            
            if user_input not in commands:
                print('invalid input')
                input('Press Enter to continue')
                continue
            
            func,message = command_functions[user_input]
            if message =='':
                success, message = func()
            if message == 'Enter the number of weeks: ':
                 display_message = func(message,'weeks')
            else:
                display_message = func(message)

    def run_monthly_repeats(self):
        """Executes the interactive setup for monthly repeat patterns."""
        print("This feature is under development. Please check back later.")
        input("Press Enter to return to the main menu...")

    def __basic_input(self,message,commands,history_file_name,example=None,current_dir='',field_pair=None):
        """Wraps auto-completer input prompt handling and menu status header.

        Args:
            message: Prompt text shown to user.
            commands: List of auto-completable string commands.
            history_file_name: File key for storing command history.
            example: Footer instructions or usage hints displayed under prompt.
            current_dir: Sub-path append string for location breadcrumb display.
            field_pair: Field key-value context for complex input fields.

        Returns:
            str: Normalized lower-case string command entered by the user.
        """
        auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        if field_pair is None:
            print(Fore.LIGHTBLACK_EX+self.__shelf.display_state().replace('  :',':')+Fore.RESET)
            self.__update_habit_inputs.display_copied_habit()
        else:
            auto_completer.set_has_status(True)
        return auto_completer.prompt_input(message,commands,example,location=f"Home/RepeatHabit"+current_dir,field_pair=field_pair).lower()

    def run(self):
        """Launches the main Repeat Habit controller interactive navigation loop.

        Routes commands to sub-menus for copying habit templates or launching daily,
        weekly, custom, and monthly recurrence engine wizards.
        """
        command_functions = {
            'copy habit from shelf':self.__update_habit_inputs.collect_copied_habit,
            'run daily repeat pattern':self.run_daily_repeats,
            'run weekly repeat pattern':self.run_week_repeats,
            'run custom repeat pattern':self.run_custom_repeats,
            'run monthly repeat pattern':self.run_monthly_repeats,  
        }
        commands = list(command_functions.keys())
        while True:
            clear_screen()
            history_file_name = 'repeat_habit'
            user_input = self.__basic_input("Enter command: ",commands,history_file_name,'[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands')
            match user_input:
                case 'esc':
                    break
                case 'clear':
                    clear_screen()
                case 'help':
                    ran_common_functions('help',history_file_name='habit_repeats')
                    continue
            if user_input=='copy habit from shelf':
                self.__update_habit_inputs.set_habit_is_copied_once(True)
                funct = command_functions[user_input]
                funct()
            
            if self.__update_habit_inputs.get_habit() is None:
                print('Copy the habit sesssion from the shelf before completing it')
                input('Press Enter to continue')
                continue

            if user_input not in commands:
                print('invalid input')
                continue
            
            func = command_functions[user_input]
            func()
            clear_screen()