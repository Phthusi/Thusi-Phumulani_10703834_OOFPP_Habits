from .update_habit_inputs import UpdateHabitInputs,retry_until_success,ran_common_functions, AutoCompleter
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import ProgressBar
from ..shelf import Shelf
from pathlib import Path
from colorama import Fore
BASE_DIR = Path(__file__).resolve().parent

class UpdateHabit:
    def __init__(self):
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__form = self.__update_habit_inputs.get_main_form()
        self.progress_bar = ProgressBar(2)
        self.__current_filled_fields = self.__form.number_of_filled_fields()
        self.__shelf = Shelf()

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
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state().replace('  :',':')}')
        self.__update_habit_inputs.display_copied_habit()
        return autocompleter.prompt_input(message,location=f"Home/UpdateHabit").lower()

    def run(self):
        command_functions = {
            'number of fields to update':[
                self.__update_habit_inputs.set_habit_field_number,
                'Enter the number of fields: '
            ],
            'choose fields to update':[
                self.__update_habit_inputs.choose_fields_to_update,
                self.__update_habit_inputs.set_fields_to_update,
                'Enter the fields you want to update: '
            ],
            'complete update':[
                self.__update_habit_inputs.update
            ],
            'copy habit from shelf':[
                self.__update_habit_inputs.collect_copied_habit,
            ],
            'view habit to update':[
                self.__update_habit_inputs.view_habit_to_update
            ]
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'update_habit'
            user_input = self.__my_input("Enter command: ",history_file_name,commands)
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            if user_input in commands[:1]:
                funct,message = command_functions[user_input]
                funct(message)
            
            if user_input=='choose fields to update':
                funct1,funct2,message = command_functions[user_input]
                funct1(message)
                try:
                    funct2()
                except Exception as e:
                    pass
            elif user_input=='complete update':
                funct = command_functions[user_input][0]
                funct()
            
            elif user_input=='copy habit from shelf':
                funct = command_functions[user_input][0]
                funct()
            
            elif user_input=='view habit to update':  
                funct = command_functions[user_input][0]
                funct()

            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")

            # update the progress thingy