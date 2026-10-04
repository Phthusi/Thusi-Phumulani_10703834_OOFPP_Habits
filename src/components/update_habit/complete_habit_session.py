from .update_habit_inputs import UpdateHabitInputs,ran_common_functions, AutoCompleter
from ..ui.terminal_utils import clear_screen
from ..shelf import Shelf
from pathlib import Path
from colorama import Fore

BASE_DIR = Path(__file__).resolve().parent

class CompleteHabitSession:
    """Manages an interactive terminal session for marking habits as completed.

    Handles user menu selection, integrates autocompletion history, retrieves copied
    habits from the shelf storage, displays current habit state, and updates completion
    statuses in memory and persistence layers.
    """
    def __init__(self):
        """Initializes dependencies for managing habit updates and shelf interaction."""
        self.__update_habit_inputs = UpdateHabitInputs()
        self.__shelf = Shelf()

    def __my_input(self,message,history_file_name,commands,example=None):
        """Helper method to prompt for user input with autocompletion and status displays.

        Args:
            message (str): Text prompt shown to the user.
            history_file_name (str): Relative path/filename for persistent command history.
            commands (list[str]): Available command strings for fuzzy autocompletion.
            example (str, optional): Keyboard shortcuts or usage guidance text. Defaults to None.

        Returns:
            str: Normalized lower-case input string entered by the user.
        """
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state().replace('  :',':')}')
        self.__update_habit_inputs.display_copied_habit()
        return autocompleter.prompt_input(message,location=f"Home/CompleteSession",example=example).lower()

    def run(self):
        """Executes the main interactive loop for completing habit sessions.

        Clears the terminal, prompts for command entry, validates common shortcut commands
        ('esc', 'clear', 'help'), enforces requirement checks for active habit selection,
        and triggers actions like copying habits from shelf, viewing details, or saving
        completed states.
        """
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

            user_input = self.__my_input("Enter command: ",history_file_name,commands,example=f'{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
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
                if success=='success':
                    habit = self.__update_habit_inputs.get_habit()
                    id = habit.get_id()
                    name = habit.get_name()
                    datetime = habit.get_start_date()
                    duration = habit.get_session_duration()
                    status = 'COMPLETED'
                    periodicity = habit.get_periodicity()
                    self.__shelf.preserve_habit((id,name,datetime,duration,status,periodicity))
            elif user_input=='view habit to update':  
                funct = command_functions[user_input][0]
                funct()

            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")