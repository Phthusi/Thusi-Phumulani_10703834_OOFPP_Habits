from .data.db_manager import DB_Interface,Habits
from .functionality_units.add_unit.add_habit import Add_Habit
from .functionality_units.delete_unit.delete_habit import DeleteHabit
from .functionality_units.time_project.time_manager import HabitDateTimeManager
from .functionality_units.update_habit.update_habit_inputs import UpdateHabitInputs
from .functionality_units.update_habit.update_habit import UpdateHabit
from .functionality_units.search_unit.search_habit_inputs import SearchHabitInputs
from .functionality_units.search_unit.search_habit import SearchHabit
from .functionality_units.ui.command_autocomplete import AutoCompleter,update_habit_statuses
from .functionality_units.ui.terminal_utils import clear_screen
from .functionality_units.analytics_unit.habits_analytics import Analytics
# from .functionality_units.habit_repeats_unit.habit_repeats import HabitRepeats
from pathlib import Path
from .functionality_units.ui.terminal_utils import clear_screen
from .functionality_units.shelf import Shelf
from .functionality_units.update_habit.complete_habit_session import CompleteHabitSession

BASE_DIR = Path(__file__).resolve().parent

def my_input(message,history_file_name,commands,field_pair=None,base='Home',example=None):
    auto_completer = AutoCompleter(BASE_DIR / f"main_history/{history_file_name}",commands)
    auto_completer.set_has_status(True)
    return auto_completer.prompt_input(message,location=f"{base}",field_pair=field_pair,example=example).lower()

def main_program():
    search_habits = SearchHabit()
    update_habits = UpdateHabit()
    add_habits = Add_Habit()
    # habit_repeats = HabitRepeats()
    delete_habit = DeleteHabit()
    complete_habit_session = CompleteHabitSession()
    shelf = Shelf()
    analytics = Analytics()
    analytics.find_statuses()

    while True:
        commands = ['update habit','search habit(s)','add habit','esc','repeat habits','delete habit','complete session','analytics']
        history_file_name = 'main'
        clear_screen()
        user_input = my_input('Enter command: ',history_file_name,commands,example=f'Longest Streak  : {analytics.longest_streak()}\nCurrent Streak  : {analytics.current_streak()}\nCompletion Rate : {analytics.completion_rate()}\nTotal Missed Sessions   : {analytics.total_missed_sessions()}\nTotal Completed Sessions: {analytics.total_completed_sessions()}\n{shelf.display_state().replace('\n','\n ')}\n{'-'*105}\n NB: ⌨️  [↑/↓] History   •   [Enter] Select   •   [Esc]  Exit  • Press space to view available commands\n{'-'*105}')
        match user_input:
            case 'update habit':
                update_habits.run()
            case 'search habit(s)':
                search_habits.run()
            case 'add habit':
                add_habits.run()
            # case 'repeat habits':
            #     habit_repeats.run()
            case 'delete habit':
                delete_habit.run()
            case 'analytics':
                analytics.display_detailed_analytics()
            case 'complete session':
                complete_habit_session.run()
                continue
            case 'clear':
                clear_screen()
            case 'esc':
                break
            case default:
                print(f'\'{user_input}\' invalid')
                input('press enter to continue')
    clear_screen()

update_habit_statuses()
def main():
    main_program()
    update_habit_statuses()