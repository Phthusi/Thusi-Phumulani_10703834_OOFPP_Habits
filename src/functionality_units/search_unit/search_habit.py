from .search_habit_inputs import SearchHabitInputs,retry_until_success,ran_common_functions, AutoCompleter
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import ProgressBar
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class SearchHabit:
    
    def __init__(self):
        self.__search_habit_inputs = SearchHabitInputs()
        self.__form = self.__search_habit_inputs.get_main_form()
        self.progress_bar = ProgressBar(5)
        self.__current_filled_fields = self.__form.number_of_filled_fields()


    def __my_input(self,message,history_file_name,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        if self.__current_filled_fields != self.__form.number_of_filled_fields():
            self.progress_bar.increase_progress_percentage(self.__form.number_of_filled_fields())
            self.__current_filled_fields = self.__form.number_of_filled_fields()
        # print("Flow          : ✅ Find ID --→ ✅ Num Fields --→ ❌ Choose Fields --→ ❌ Complete")
        self.progress_bar.display_progress_bar()
        print('Pipe Status   : ❌ Empty')
        self.__update_habit_inputs.display_grabbed_habit()
        return autocompleter.prompt_input(message,location=f"Home/SearchHabit").lower()
