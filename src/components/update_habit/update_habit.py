from .update_habit_inputs import UpdateHabitInputs,retry_until_success,ran_common_functions, AutoCompleter
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import Form, ProgressBar
from ..shelf import Shelf
from pathlib import Path
from colorama import Fore
BASE_DIR = Path(__file__).resolve().parent

class UpdateHabit:
    def __init__(self):
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__form = self.__update_habit_inputs.get_main_form()
        self.__current_filled_fields = self.__form.number_of_filled_fields()
        self.__shelf = Shelf()

    def __my_input(self,message,history_file_name,commands,example=None):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        if self.__current_filled_fields != self.__form.number_of_filled_fields():
            self.__current_filled_fields = self.__form.number_of_filled_fields()
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state().replace('  :',':')}')
        self.__update_habit_inputs.display_copied_habit()
        Fore.RESET
        if len(self.__update_habit_inputs.get_display_form().get_filled_fields()) == 0:
            display_map = """
[cyan]📌 LEVEL 1: PARAMETERS[/] [green]{name}[/] Name [blue] {start_datetime}[/] Start Datetime [green] {duration}[/] Duration  | [cyan]🔒 LEVEL 2: ACTION(S) [/] Complete update"""
            self.__update_habit_inputs.get_display_form().set_display_map(display_map)
        else:
            display_map = """
            [cyan]📌 LEVEL 1: PARAMETERS[/] [green]{name}[/] Name [blue] {start_datetime}[/] Start Datetime [green] {duration}[/] Duration  | [cyan]🔓 LEVEL 2: ACTION(S) [/] Complete update"""
            self.__update_habit_inputs.get_display_form().set_display_map(display_map)

        display_map = self.__update_habit_inputs.get_display_form().get_display_map().replace('[/]','{Fore.WHITE}').replace('[green]','{Fore.GREEN}').replace('[cyan]','{Fore.CYAN}').replace('[blue]','{Fore.BLUE}')
        print(display_map.format_map(globals()))
        return autocompleter.prompt_input(message,location=f"Home/UpdateHabit",example=example).lower()

    def run(self):
        command_functions = {
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
            user_input = self.__my_input("Enter command: ",history_file_name,commands,example=f'{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
    
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
                input('Press Enter to exit')