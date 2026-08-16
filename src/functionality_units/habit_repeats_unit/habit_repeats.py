from pathlib import Path
from colorama import Fore

from ...data.db_manager import CompleteHabit
from ..ui.command_autocomplete import AutoCompleter, Form, ProgressBar
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message, clear_screen
from ..shelf import Shelf
# from .habit_repeats_models import (
#     WeekPatternManager, 
#     MonthPatternManager, 
#     MonthsPatternManager
# )
from .habit_repeats_validator import WeekPatternValidator, MonthPatternValidator

BASE_DIR = Path(__file__).resolve().parent


class HabitRepeatsManager:

    def __init__(self, base_directory=None):
        self.__BASE_DIR = base_directory or BASE_DIR
        self.__habit = None
        self.__copied_habit_status = "No habit has been copied from the shelf, please copy the habit from the shelf"
        self.__shelf = Shelf()

        display_map = """
[bold cyan]📌 LEVEL 1: PARAMETERS[/] [green]{week_pattern}[/] Week Pattern [bold blue] {month_pattern}[/] Month Pattern [green] {months_pattern}[/] Months Pattern  |  [bold cyan]🔒 LEVEL 2: ACTION(S) [/] Save"""

        self.__main_form = Form(
            {field: False for field in [
                'week_pattern', 'week_pattern_name',
                'month_pattern', 'month_pattern_name',
                'months_pattern', 'months_pattern_name'
            ]},
            display_map
        )

        self.progress_bar = ProgressBar(7)
        self.__current_filled_fields = 0

        # Managers & Validators
        # self.__week_pattern_manager = WeekPatternManager()
        self.__week_pattern_validator = WeekPatternValidator()
        # self.__month_pattern_manager = MonthPatternManager()
        self.__month_pattern_validator = MonthPatternValidator()
        # self.__months_pattern_manager = MonthsPatternManager()

        # State storage
        self.__week_pattern_name = None
        self.__month_pattern_name = None
        self.__months_pattern_name = None

    def __display_copied_habit(self):
        """Displays status header for the staged habit."""
        if self.__habit is None:
            print(
                f"{Fore.LIGHTBLACK_EX}Status        : ❌ {self.__copied_habit_status}\n"
                f"Habit ID      : {Fore.LIGHTBLUE_EX}N/A"
            )
            return

        print(
            f"{Fore.LIGHTBLACK_EX}Status        : ✅ {self.__copied_habit_status}\n"
            f"Habit ID      : {Fore.LIGHTGREEN_EX}{self.__habit.get_id()} | Name: {self.__habit.get_name()}"
        )

    def collect_copied_habit(self):
        """Fetches the staged habit from the Shelf."""
        selected_habit_tuple = Shelf.copy_last_place_habit()

        if selected_habit_tuple is None:
            self.__habit = None
            self.__copied_habit_status = "No habit was found on the shelf. Please copy a valid habit first."
            print(f"\n{Fore.RED}⚠️ Shelf is empty or no valid habit selected.{Fore.RESET}")
            input("Press enter to continue...")
            return self.__copied_habit_status

        habit_data = {
            'id': int(selected_habit_tuple[0]),
            'name': selected_habit_tuple[1],
            'start_date': selected_habit_tuple[2],
            'session_duration': selected_habit_tuple[3],
            'status': selected_habit_tuple[4]
        }

        self.__habit = CompleteHabit(**habit_data)
        self.__copied_habit_status = "Habit has been successfully copied from the shelf"
        print(f"\n{Fore.GREEN}✅ Habit '{self.__habit.get_name()}' loaded from shelf!{Fore.RESET}")
        input("Press enter to continue...")
        return 'success...'

    def __my_input(self, message: str, history_file_name: str, commands: list, field_pair=None, example=None):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}", commands)

        # Header output
        shelf_state = self.__shelf.display_state().replace("  :", ":")
        print(f"{Fore.LIGHTBLACK_EX}{shelf_state}")
        self.__display_copied_habit()

        # Progress tracking
        filled_count = self.__main_form.number_of_filled_fields()
        if self.__current_filled_fields != filled_count:
            self.progress_bar.increase_progress_percentage(filled_count)
            self.__current_filled_fields = filled_count

        self.progress_bar.display_progress_bar(self.__main_form.get_display_map())
        autocompleter.set_has_status(True)

        modified_history = "".join([word.capitalize() for word in history_file_name.split('_')])
        return autocompleter.prompt_input(
            message,
            location=f"Home/HabitRepeats/{modified_history}",
            field_pair=field_pair,
            example=example
        ).lower()

    # -------------------------------------------------------------------------
    # STEP HANDLERS
    # -------------------------------------------------------------------------
    @retry_until_success
    def set_week_pattern_name(self, message="Enter week pattern name: "):
        clear_screen()
        history_file_name = 'week_pattern_name'
        week_pattern_name = self.__my_input(message, history_file_name, [])

        did_run_common_func = ran_common_functions(week_pattern_name)
        if not did_run_common_func:
            return True, find_message(week_pattern_name)

        success, msg = self.__week_pattern_validator.is_name_pattern_valid(week_pattern_name)
        if success:
            self.__main_form.set_field_status('week_pattern_name', True)
            self.__week_pattern_name = week_pattern_name
        return success, msg

    @retry_until_success
    def set_week_pattern(self, message="Enter days (e.g. mon tue fri): "):
        clear_screen()
        if self.__week_pattern_name is None:
            return False, 'First enter the week pattern name'

        history_file_name = 'week_pattern'
        commands = ['mon', 'tue', 'wed', 'thurs', 'fri', 'sat', 'sun']
        week_pattern = self.__my_input(message, history_file_name, commands)

        did_run_common_func = ran_common_functions(week_pattern)
        if not did_run_common_func:
            return True, find_message(week_pattern)

        weekdays = set(week_pattern.split(' '))
        is_valid = [day in commands for day in weekdays]

        if all(is_valid):
            success, msg = self.__week_pattern_manager.save_week_pattern(self.__week_pattern_name, weekdays)
            if success:
                self.__main_form.set_field_status('week_pattern', True)
            return success, msg

        invalid_day = list(weekdays)[is_valid.index(False)]
        return False, f"'{invalid_day}' is not a valid weekday"

    @retry_until_success
    def set_month_pattern_name(self, message="Enter month pattern name: "):
        clear_screen()
        history_file_name = 'month_pattern_name'
        month_pattern_name = self.__my_input(message, history_file_name, [])

        did_run_common_func = ran_common_functions(month_pattern_name)
        if not did_run_common_func:
            return True, find_message(month_pattern_name)

        success, msg = self.__month_pattern_validator.is_name_pattern_valid(month_pattern_name)
        if success:
            self.__main_form.set_field_status('month_pattern_name', True)
            self.__month_pattern_name = month_pattern_name
        return success, msg

    @retry_until_success
    def set_month_pattern(self, message="Enter 4 week names (e.g. week1 week2 skip week3): "):
        clear_screen()
        if self.__month_pattern_name is None:
            return False, 'First enter the month pattern name'

        available_weeks = self.__week_pattern_manager.get_all_names()
        commands = available_weeks + ['skip']

        history_file_name = 'month_pattern'
        month_input = self.__my_input(message, history_file_name, commands, example="week1 week3 skip week50")

        did_run_common_func = ran_common_functions(month_input)
        if not did_run_common_func:
            return True, find_message(month_input)

        selected_weeks = month_input.split(' ')
        if len(selected_weeks) != 4:
            return False, f"A month pattern requires exactly 4 weeks (got {len(selected_weeks)})."

        invalid_weeks = [w for w in selected_weeks if w not in commands]
        if invalid_weeks:
            return False, f"Unknown week pattern(s): {', '.join(invalid_weeks)}"

        success, msg = self.__month_pattern_manager.save_month_pattern(self.__month_pattern_name, selected_weeks)
        if success:
            self.__main_form.set_field_status('month_pattern', True)
        return success, msg

    @retry_until_success
    def set_months_pattern_name(self, message="Enter months pattern name: "):
        clear_screen()
        history_file_name = 'months_pattern_name'
        months_pattern_name = self.__my_input(message, history_file_name, [])

        did_run_common_func = ran_common_functions(months_pattern_name)
        if not did_run_common_func:
            return True, find_message(months_pattern_name)

        self.__months_pattern_name = months_pattern_name
        self.__main_form.set_field_status('months_pattern_name', True)
        return True, "Months pattern name set successfully"

    @retry_until_success
    def set_months_pattern(self, message="Enter month pattern sequence (e.g. month1 skip month2): "):
        clear_screen()
        if self.__months_pattern_name is None:
            return False, 'First enter the months pattern name'

        available_months = self.__month_pattern_manager.get_all_names()
        commands = available_months + ['skip']

        history_file_name = 'months_pattern'
        months_input = self.__my_input(message, history_file_name, commands, example="month1 skip month2")

        did_run_common_func = ran_common_functions(months_input)
        if not did_run_common_func:
            return True, find_message(months_input)

        selected_months = months_input.split(' ')
        invalid_months = [m for m in selected_months if m not in commands]
        if invalid_months:
            return False, f"Unknown month pattern(s): {', '.join(invalid_months)}"

        success, msg = self.__months_pattern_manager.save_months_pattern(self.__months_pattern_name, selected_months)
        if success:
            self.__main_form.set_field_status('months_pattern', True)
        return success, msg

    # -------------------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------------------
    def run(self):
        command_functions = {
            'copy habit from shelf': self.collect_copied_habit,
            'set week pattern name': lambda: self.set_week_pattern_name(),
            'set week pattern': lambda: self.set_week_pattern(),
            'set month pattern name': lambda: self.set_month_pattern_name(),
            'set month pattern': lambda: self.set_month_pattern(),
            'set months pattern name': lambda: self.set_months_pattern_name(),
            'set months pattern': lambda: self.set_months_pattern(),
        }

        while True:
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'habit_repeats_manager'

            user_input = self.__my_input("Enter command: ", history_file_name, commands)

            # Common functions execution check
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func is not None:
                if user_input == 'esc':
                    break
                continue

            # Execute registered command
            if user_input in command_functions:
                funct = command_functions[user_input]
                funct()
            else:
                print(f"\n'{user_input}' is not in the given options, please press space to see your options.")
                input('Press enter to continue...')