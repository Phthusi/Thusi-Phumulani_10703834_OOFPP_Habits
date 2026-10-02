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

    def __my_input(self,message,history_file_name,commands,example=None):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        if self.__current_filled_fields != self.__form.number_of_filled_fields():
            self.progress_bar.increase_progress_percentage(self.__form.number_of_filled_fields())
            self.__current_filled_fields = self.__form.number_of_filled_fields()
        self.__search_habit_inputs.display_copied_habit()
        return autocompleter.prompt_input(message,location=f"Home/SearchHabit",example=example).lower()

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
            user_input = self.__my_input("Enter command: ",history_file_name,commands,example=f'{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************  
            if user_input not in command_functions.keys() or user_input=='':
                print(f'\'{user_input}\' is not a valid command')
                input('Press Enter to continue')
                continue
            function = command_functions[user_input][0]
            function()