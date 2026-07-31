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

    def stages(self):
        stages = [
            "[_______find habit ID_____] ---→",
            "[___number of fields to update___] ---→",
            "[___choose fields to update___] ---→",
            "[__complete update__]"
        ]
        # [✅ find habit ID] ---→ [✅ number of fields to update] ---→ [🔄 choose fields to update] ---→ [⬜ complete update]

    def __my_input(self,message,history_file_name,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        if self.__current_filled_fields != self.__form.number_of_filled_fields():
            self.progress_bar.increase_progress_percentage(self.__form.number_of_filled_fields())
            self.__current_filled_fields = self.__form.number_of_filled_fields()
        # self.progress_bar.display_progress_bar()
        print('Shelf Status    : ❌ Empty')
        print('Results Status  : ❌ Empty')
        print('Last Search     : time before 15:00')
        # print(f'''sorted        : N/A''') this is for viewing
        self.__search_habit_inputs.display_grabbed_habit()
        return autocompleter.prompt_input(message,location=f"Home/SearchHabit").lower()

    def run(self):
        command_functions = {
            'get habit(s)':[
                self.__search_habit_inputs.find_habits
            ],
            'view selected habit':[
                self.__search_habit_inputs.view_selected_habit
            ]
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'search_habit'
            user_input = self.__my_input("Enter command: ",history_file_name,commands)
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************  
            if user_input not in command_functions.keys():
                continue
            x= command_functions[user_input][0]
            x()