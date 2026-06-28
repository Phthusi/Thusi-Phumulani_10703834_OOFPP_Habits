from .update_habit_inputs import UpdateHabitInputs,retry_until_success,ran_common_functions,AutoCompleter
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class UpdateHabit:
    def __init__(self):
        self.__update_habit_inputs = UpdateHabitInputs()

    def __my_input(self,message,history_file_name,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        return autocompleter.prompt_input(message,location=f"Home/UpdateHabit").lower()

    def run(self):
        command_functions = {
            'find habit':[
                self.__update_habit_inputs.find_habit_id,
                'Enter habit ID: '
            ],
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
            ]
        }

        while True:        
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
            if user_input in commands[:2]:
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
                
            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
