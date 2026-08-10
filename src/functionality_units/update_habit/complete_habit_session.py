from .update_habit_inputs import UpdateHabitInputs,retry_until_success,ran_common_functions, AutoCompleter
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import ProgressBar
from ..shelf import Shelf
from pathlib import Path
from colorama import Fore

BASE_DIR = Path(__file__).resolve().parent

class CompleteHabitSession:
    def __init__(self):
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__shelf = Shelf()

    def __my_input(self,message,history_file_name,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state().replace('  :',':')}')
        self.__update_habit_inputs.display_copied_habit()
        return autocompleter.prompt_input(message,location=f"Home/UpdateHabit").lower()

    def run(self):
        command_functions = {
            'complete update':None,
            'copy habit from shelf':[
                self.__update_habit_inputs.collect_copied_habit,
            ],
            'view habit to update':[
                self.__update_habit_inputs.view_habit_to_update
            ]
        }

        commands = list(command_functions.keys())
        history_file_name = 'update_habit'
        while True:        
            clear_screen()

            user_input = self.__my_input("Enter command: ",history_file_name,commands)
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            if user_input=='copy habit from shelf':
                funct = command_functions[user_input][0]
                funct()
            
            if self.__update_habit_inputs.get_habit() is None:
                print('Copy the habit sesssion from the shelf before completing it')
                input('Press Enter to continue')
                continue

            if user_input=='complete update':
                success,message = self.__update_habit_inputs.get_habit().complete_habit()
                
                input(f'{message}\nPress Enter to continue')

            elif user_input=='view habit to update':  
                funct = command_functions[user_input][0]
                funct()

            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")