from .data.db_manager import DB_Interface,Habits
from .functionality_units.delete_unit.delete_habit import DeleteHabit
from .functionality_units.time_project.time_manager import HabitDateTimeManager
from .functionality_units.update_habit.update_habit_inputs import UpdateHabitInputs
from .functionality_units.update_habit.update_habit import UpdateHabit
from .functionality_units.search_unit.search_habit_inputs import SearchHabitInputs
import threading
import time

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


def main_program():
    # x = DeleteHabit()
    # x.delete("Enter the id of the habit you want to delete")
    # x = UpdateHabitInputs()
    # x.find_habit_id('Enter id: ')
    # x.set_habit_field_number('Enter the number of fields: ')
    # x.choose_fields_to_update('Enter the fields you want to update: ')
    # x.set_fields_to_update()
    # x.update()
    x = UpdateHabit()
    x.run()
    # x = SearchHabitInputs()
    # x.find_habits('Enter habit: ')

def main():
    main_program()