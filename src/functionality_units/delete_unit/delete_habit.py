from ...data.db_manager import CompleteHabit, Habits
from ..ui.command_autocomplete import AutoCompleter
from ..ui.terminal_utils import ran_common_functions, retry_until_success,clear_screen
from ..shelf import Shelf
from colorama import Fore

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class DeleteHabit:

    def __init__(self):
        self.__habits = Habits()
        self.__habit = None
        self.__copied_habit_status = "No habit has been copied from the shelf, please copy the habit from the shelf"
        self.__shelf = Shelf()

    def __my_input(self,message,history_file_name,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        print(f'{Fore.LIGHTBLACK_EX}{self.__shelf.display_state().replace('  :',':')}')
        self.__display_copied_habit()
        return autocompleter.prompt_input(message,location=f"Home/DeleteHabit").lower()

    def __display_copied_habit(self):
        if self.__habit is None:
            print(f'''{Fore.LIGHTBLACK_EX}Status        : ❌ {self.__copied_habit_status}
Habit ID      : {Fore.LIGHTBLUE_EX}N/A''')
            return
        print(f'''{Fore.LIGHTBLACK_EX}Status        : ✅ {self.__copied_habit_status}
Habit ID      : {Fore.LIGHTGREEN_EX}{self.__habit.get_id()}''')

    def collect_copied_habit(self):
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
        return self.__habit.delete_habit()

    def delete(self):
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
        command_functions = {
            'delete habit':self.delete,
            'copy habit from shelf':
                self.collect_copied_habit,
        }

        while True:        
            clear_screen()
            commands = list(command_functions.keys())
            history_file_name = 'delete_habit'
            user_input = self.__my_input("Enter command: ",history_file_name,commands)
            # ********* start of common functions ************        
            did_run_common_func = ran_common_functions(user_input)
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
