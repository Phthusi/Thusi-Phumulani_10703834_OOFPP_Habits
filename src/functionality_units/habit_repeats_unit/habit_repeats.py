from ..ui.terminal_utils import ran_common_functions, retry_until_success,find_message
from .habit_repeats_models import WeekPatternManager, MonthPatternManager
from .habit_repeats_validator import WeekPatternValidator, MonthPatternValidator
from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.command_autocomplete import ProgressBar
from pathlib import Path
from ..view import View

BASE_DIR = Path(__file__).resolve().parent
class HabitRepeats:
    def __init__(self):
        self.progress_bar = ProgressBar(4)
        self.__week_pattern_manager = WeekPatternManager()
        # self.__week_pattern_validator = WeekPatternValidator()
        
        self.__week_pattern_name = None
        # self.__current_filled_fields = self.__form.number_of_filled_fields()

    def __my_input(self,message,history_file_name,example,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        # if self.__current_filled_fields != self.__form.number_of_filled_fields():
        #     self.progress_bar.increase_progress_percentage(self.__form.number_of_filled_fields())
        #     self.__current_filled_fields = self.__form.number_of_filled_fields()

        self.progress_bar.display_progress_bar()
        # self.__update_habit_inputs.display_grabbed_habit()
        return autocompleter.prompt_input(message,location=f"Home/UpdateHabit",example=example).lower()

    @retry_until_success
    def set_name(self):
        history_file_name = 'set_name'
        commands = []
        user_input = self.__my_input('Enter the week pattern name: ',history_file_name,example='Input example: week1',commands=commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        success,message =  self.__week_pattern_validator.is_name_pattern_valid(user_input)
        if success:
            return success,message
        return success,message

    @retry_until_success
    def set_week_pattern(self):
        history_file_name = 'week_pattern'
        commands = ['mon','tue','wed','thurs','fri','sat','sun']
        user_input = self.__my_input('Enter the week pattern: ',history_file_name,example='Input Example: mon tue sun',commands=commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(user_input)
        message_to_display = find_message(user_input)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        weekdays = set(user_input.split(' '))
        is_valid_weekdays = list(map(lambda weekday: weekday in commands,weekdays))
        
        if all(is_valid_weekdays):
            self.set_name()
            if self.__week_pattern_name is None:
                message = 'week pattern name was not set'
                return success,message
            success,message = self.__week_pattern_manager.save_week_pattern(self.__week_pattern_name,weekdays)
            return success,message
        return False,f'\'{weekdays[is_valid_weekdays.index(False)]}\' is not valid'
        

    @retry_until_success
    def set_month_pattern(self):
        history_file_name = 'week_pattern'
        commands = ['mon','tue','wed','thurs','fri','sat','sun']


    @retry_until_success
    def set_months_pattern(self):
        history_file_name = 'week_pattern'
        commands = ['mon','tue','wed','thurs','fri','sat','sun']


    @retry_until_success
    def create_custom_pattern(self):
        pass

    @retry_until_success
    def create_once_a_week_pattern(self):
        pass

    @retry_until_success
    def create_once_a_month_pattern(self):
        pass

    @retry_until_success
    def create_daily_pattern(self):
        pass

    def run(self):
        self.set_week_pattern()

