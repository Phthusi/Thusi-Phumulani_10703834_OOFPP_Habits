from .data.db_manager import DB_Interface,Habits
from .functionality_units.add_unit.add_habit import Add_Habit
from .functionality_units.delete_unit.delete_habit import DeleteHabit
from .functionality_units.time_project.time_manager import HabitDateTimeManager
from .functionality_units.update_habit.update_habit_inputs import UpdateHabitInputs
from .functionality_units.update_habit.update_habit import UpdateHabit
from .functionality_units.search_unit.search_habit_inputs import SearchHabitInputs
from .functionality_units.search_unit.search_habit import SearchHabit
from .functionality_units.ui.command_autocomplete import AutoCompleter
from .functionality_units.ui.terminal_utils import clear_screen
from .functionality_units.habit_repeats_unit.habit_repeats import HabitRepeats
from pathlib import Path
from .functionality_units.ui.terminal_utils import clear_screen
from .functionality_units.shelf import Shelf
import threading
import time

BASE_DIR = Path(__file__).resolve().parent

running = True
def background_task():
    db_interface = DB_Interface()
    habits = Habits()

    while running:
        saved_habits = habits.get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])
        habit_datetime_manager = HabitDateTimeManager()
        for habit in saved_habits:
            id, name, start_datetime, duration, status = habit
            new_status = habit_datetime_manager.determine_habit_status(start_datetime,duration)
            if new_status!=status:
                db_interface.update_habit(id,**{'status':new_status}) 

def my_input(message,history_file_name,commands,field_pair=None,base='Home/',example=None):
    auto_completer = AutoCompleter(BASE_DIR / f"main_history/{history_file_name}",commands)
    auto_completer.set_has_status(True)
    modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
    return auto_completer.prompt_input(message,location=f"{base}{modified_history_file_name}",field_pair=field_pair,example=example).lower()


def main_program():
    # x = DeleteHabit()
    # x.delete("Enter the id of the habit you want to delete")
    # x = UpdateHabitInputs()
    # x.find_habit_id('Enter id: ')
    # x.set_habit_field_number('Enter the number of fields: ')
    # x.choose_fields_to_update('Enter the fields you want to update: ')
    # x.set_fields_to_update()
    # x.update()
    # x = UpdateHabit()
    # x.run()
    # x = SearchHabitInputs()
    # x.find_habits('Enter habit: ')
    # x = SearchHabit()
    # x.run()

    search_habits = SearchHabit()
    update_habits = UpdateHabit()
    add_habits = Add_Habit()
    habit_repeats = HabitRepeats()
    shelf = Shelf()

    while True:
        commands = ['update habit','search habit(s)','add habit','esc','repeat habits']
        history_file_name = 'main'
        clear_screen()
        user_input = my_input('Enter command: ',history_file_name,commands,example=f' {shelf.display_state().replace('\n','\n ')}\n NB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands')
        match user_input:
            case 'update habit':
                update_habits.run()
            case 'search habit(s)':
                search_habits.run()
            case 'add habit':
                add_habits.run()
            case 'repeat habits':
                habit_repeats.run()
            case 'delete habit':
                pass
            case 'clear':
                clear_screen()
            case 'esc':
                break
            case default:
                print(f'\'{user_input}\' invalid')
    clear_screen()

def main():
    main_program()