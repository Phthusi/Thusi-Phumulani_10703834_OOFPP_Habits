from .habit_repeats_models import WeekPatternManager,WeekPattern,MonthPatternManager,MonthPattern
from .habit_repeats_validator import WeekPatternValidator,MonthPatternValidator
from ..habit_input import Habit_Inputs
from pathlib import Path
from ...data.db_manager import CompleteHabit, Habits
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.command_autocomplete import ProgressBar
from ..ui.terminal_utils import ran_common_functions, retry_until_success
from ..update_habit.update_habit_inputs import UpdateHabitInputs
from colorama import Fore, Style, Back

BASE_DIR = Path(__file__).resolve().parent

class HabitRepeats:
    def __init__(self):
        self.__habit_inputs = Habit_Inputs(BASE_DIR)
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__week_pattern_manager = WeekPatternManager()
        self.__month_pattern_manager = MonthPatternManager()
        self.__week_pattern = WeekPattern('default')
        self.__week_pattern_validator = WeekPatternValidator(self.__week_pattern)
        self.__month_pattern = MonthPattern('default')
        self.__month_pattern_validator = MonthPatternValidator(self.__week_pattern)
        self.progress_bar = ProgressBar(7)
        self.__levels = {'level1':'➡️','level2':' ','level3':' '}
        self.display_map = """
    ----------------------------------------------------------------------------------------------------------------------------
{level1}   [bold cyan]📌 LEVEL 1: PARAMETERS[/] [green]{week_pattern_name}[/] Week Pattern Name    {week_pattern} Week Pattern
    ----------------------------------------------------------------------------------------------------------------------------
{level2}   [bold cyan]📌 LEVEL 2: PARAMETERS[/] [green]{month_pattern_name}[/] Month Pattern Name   {month_pattern} Month Pattern
    ----------------------------------------------------------------------------------------------------------------------------
{level3}   [bold cyan]📌 LEVEL 3: PARAMETERS[/] [green]{months_pattern}[/] Months Pattern
    ---------------------------------------------------------------------------------------------------------------------------- 
    [bold cyan]🔒 LEVEL 4: ACTION(S) [/] Save"""
        self.__form = Form({field: False for field in ['week_pattern_name','week_pattern','month_pattern','month_pattern_name','months_pattern']},self.display_map,levels=self.__levels)
        self.__current_filled_fields = self.__form.number_of_filled_fields()

    def __my_input(self,message,history_file_name,commands,field_pair=None,example=None,multiple_values=''):
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
        match no_of_filled_fields:
            case 2:
                self.__levels = {'level1':' ','level2':'➡️','level3':' '}
            case 4:
                self.__levels = {'level1':' ','level2':' ','level3':'➡️'}

    def __set_habit_week_pattern_name(self,message,field_pair=None):
        history_file_name='week_pattern_name'
        commands = []
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Input Format  : YYYY-MM-DD HH:MM\nInput Example : 2026-06-30 16:45\nyear = 2026, month = June, day = 30th, time= 4pm, 45 minutes\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()

    @retry_until_success
    def set_habit_week_pattern_name(self,message):
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
        history_file_name='week_pattern'
        commands = []
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        multiple_values = f"\nCurrent Value list : {Fore.LIGHTBLUE_EX if self.__week_pattern.week_patterns is None else Fore.LIGHTGREEN_EX}{self.__week_pattern.week_patterns if self.__week_pattern.week_patterns is not None else 'N/A'}{Fore.RESET}"
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Input Format  : YYYY-MM-DD HH:MM\nInput Example : 2026-06-30 16:45\nyear = 2026, month = June, day = 30th, time= 4pm, 45 minutes\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',multiple_values=multiple_values).lower()

    @retry_until_success
    def set_habit_week_pattern(self,message):
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
        history_file_name='month_pattern'
        commands = self.__week_pattern.week_patterns.keys()
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        multiple_values = f"\nCurrent Value list : {Fore.LIGHTBLUE_EX if self.__month_pattern.monthPatterns is None else Fore.LIGHTGREEN_EX}{self.__month_pattern.monthPatterns if self.__month_pattern.monthPatterns is not None else 'N/A'}{Fore.RESET}"
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Input Format  : YYYY-MM-DD HH:MM\nInput Example : 2026-06-30 16:45\nyear = 2026, month = June, day = 30th, time= 4pm, 45 minutes\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands',multiple_values=multiple_values).lower()

    @retry_until_success
    def set_habit_month_pattern(self,message):
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
        history_file_name='month_pattern_name'
        commands = []
        self.__main_autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_autocompleter.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_autocompleter.prompt_input(message,location=f"Home/RepeatHabit/{modified_history_file_name}",field_pair=field_pair,example=f'Input Format  : YYYY-MM-DD HH:MM\nInput Example : 2026-06-30 16:45\nyear = 2026, month = June, day = 30th, time= 4pm, 45 minutes\n{'-'*95}\n[↑/↓] History   •   [Enter] Select   •   [Esc] Exit  • Press space to view available commands').lower()

    @retry_until_success
    def set_habit_month_pattern_name(self,message):
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

    def run_custom_repeats(self):
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

            clear_screen()
    
    def run_week_repeats(self):
        print("This feature is under development. Please check back later.")
        input("Press Enter to return to the main menu...")

    def run_monthly_repeats(self):
        print("This feature is under development. Please check back later.")
        input("Press Enter to return to the main menu...")

    def __basic_input(self,message,commands,history_file_name,example=None):
        auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__update_habit_inputs.display_copied_habit()
        return auto_completer.prompt_input(message,commands,example,location=f"Home/RepeatHabit").lower()

    def run(self):
        command_functions = {
            'run custom repeat pattern':self.run_custom_repeats,
            'run weekly repeat pattern':self.run_week_repeats,
            'run monthly repeat pattern':self.run_monthly_repeats,  
            'copy habit from shelf':self.__update_habit_inputs.collect_copied_habit
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
            
            if user_input not in commands:
                print('invalid input')
                continue
            
            func = command_functions[user_input]
            func()
            clear_screen()