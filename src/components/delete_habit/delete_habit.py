from ...data.db_manager import CompleteHabit, Habits
from ..ui.command_autocomplete import AutoCompleter
from ..ui.terminal_utils import ran_common_functions, retry_until_success,clear_screen
from ..shelf import Shelf
from colorama import Fore
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
    
class DeleteHabit:
    """Manages the interactive terminal workflow for deleting habit records.

    Tracks active habit selection from the shelf, displays deletion status indicators,
    enforces business constraints (preventing deletion of completed or missed habits),
    and removes selected habits from persistence.

    Attributes:
        __habits (Habits): Instance managing database CRUD operations for habits.
        __habit (Optional[CompleteHabit]): The currently staged habit instance to be deleted.
        __copied_habit_status (str): UI feedback message describing shelf copy state.
        __shelf (Shelf): Shelf UI/state manager for active selection memory.
    """
    def __init__(self):
        """Initializes the DeleteHabit controller with shelf state and database connections."""
        self.__habits = Habits()
        self.__habit = None
        self.__copied_habit_status = "No habit has been copied from the shelf, please copy the habit from the shelf"
        self.__shelf = Shelf()

    def __my_input(self,message,history_file_name,commands,example=None):
        """Displays screen header, status metadata, and captures autocompleted user input.

        Args:
            message: Prompt text shown to the user.
            history_file_name: Base filename for saving CLI command history.
            commands: List of selectable command strings for autocompletion.
            example: Optional usage instructions or shortcut keys display.

        Returns:
            str: Normalized lower-case command entered by the user.
        """
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state().replace('  :',':')}')
        self.__display_copied_habit()
        return autocompleter.prompt_input(message,location=f"Home/DeleteHabit",example=example).lower()

    def __display_copied_habit(self):
        """Renders the current habit copy status and ID badge in the terminal header."""
        if self.__habit is None:
            print(f'''{Fore.LIGHTBLACK_EX}Status        : ❌ {self.__copied_habit_status}
Habit ID      : {Fore.LIGHTBLUE_EX}N/A''')
            return
        print(f'''{Fore.LIGHTBLACK_EX}Status        : ✅ {self.__copied_habit_status}
Habit ID      : {Fore.LIGHTGREEN_EX}{self.__habit.get_id()}''')

    def collect_copied_habit(self):
        """Fetches the last copied habit data tuple from the shelf and hydrates a model.

        Retrieves habit parameters from the active shelf selection, instantiates a
        `CompleteHabit` object, and updates the UI status state.

        Returns:
            str: Confirmation string 'success...' if habit loaded, or error message if shelf was empty.
        """
        selected_habit_tuple = Shelf.copy_last_place_habit()
        habit = {
            'id':int(selected_habit_tuple[0]),
            'name':selected_habit_tuple[1],
            'start_date':selected_habit_tuple[2],
            'session_duration':selected_habit_tuple[3],
            'status':selected_habit_tuple[4]
            } if selected_habit_tuple is not None else None
        habit = CompleteHabit(**habit) if not habit is None else None
        if habit is None:
            self.__copied_habit_status = 'No habit was found in the shelf, please copy the habit from the shelf'
            return self.__copied_habit_status
        
        self.__habit = habit
        self.__copied_habit_status = "Habit has been successfully copied from the shelf"
        return 'success...'
    
    def __delete_habit(self):
        """Invokes the database deletion operation on the staged habit instance.

        Returns:
            Any: Result of the model's delete operation.
        """
        return self.__habit.delete_habit()

    def delete(self):
        """Validates deletion rules and executes habit removal.

        Checks whether a habit has been staged and verifies that its status allows deletion
        (blocking deletion of 'COMPLETED', 'MISSED', or 'TO_BE_CONFIRMED' habits). If valid,
        deletes the habit, clears the shelf, and resets local state.
        """
        if self.__habit is None:
            print('There\'s no habit to delete, please copy from a habit from the shelf first')
            input('Press enter to continue')
            return
        
        if self.__habit.get_status() in ['COMPLETED','MISSED','TO_BE_CONFIRMED']:
            print('You cannot delete a habit that has been completed/missed, please copy a habit from the shelf that is not completed/missed')
            input('Press enter to continue')
            return
        
        self.__delete_habit()
        self.__shelf.empty_shelf()
        self.__habit = None
        self.__copied_habit_status = "No habit has been copied from the shelf, please copy the habit from the shelf"
        input('Habit deleted successfully\nPress enter to continue')

    def run(self):
        """Launches the interactive terminal navigation loop for deleting habits.

        Presents commands for copying habits from shelf memory and triggering deletion,
        handling screen refreshes, common utility shortcuts, and command validation.
        """
        command_functions = {
            'delete habit':self.delete,
            'copy habit from shelf':
                self.collect_copied_habit,
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'delete_habit'
            user_input = self.__my_input("Enter command: ",history_file_name,commands,example=f'{'-'*105}\nNB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input,history_file_name=history_file_name)
            if did_run_common_func==False or did_run_common_func==True:
                if user_input == 'esc':
                    break
                continue
            # ********** end of common functions ************            
            elif user_input in commands:
                funct = command_functions[user_input]
                funct()
            
            if user_input not in commands:
                print(f"'{user_input}' is not in the given options,please press space to see you options")
                input('Press enter to continue')
