from ..habit_input import Habit_Inputs
from pathlib import Path
from ...data.db_manager import CompleteHabit, Habits
from ..ui.terminal_utils import clear_screen
from ..ui.command_autocomplete import AutoCompleter

BASE_DIR = Path(__file__).resolve().parent

class Add_Habit:
    def __init__(self):
        self.__habit_inputs = Habit_Inputs(BASE_DIR)

    def is_clashing_with_any_habit(self):
        habits = [Habits().get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])] 
        datetime1 = self.__habit_inputs.get_habit().get_start_date()
        duration1 = self.__datetime_manager.convert_duration(self.__habit_inputs.get_habit().get_session_duration())
        for habit in habits: 
            id, name, start_datetime, duration, status = habit
            datetime2 = self.__datetime_manager.string_to_datetime(start_datetime)
            duration2 = self.__datetime_manager.convert_duration(duration)
            if self.__datetime_manager.is_clashing(datetime1,duration1,datetime2,duration2):
                habit_from_db = f'Habit(id={id},name={name}, start_datetime={datetime2}, session_duration={duration}, status={status})'
                habit_to_be_added = f'Habit(id={self.__habit.get_id()}, name={self.__habit.get_name()}, start_datetime={datetime1}, session_duration={self.__habit.get_session_duration()})'
                return False, f'{habit_to_be_added} cannot be saved beacuse it clashes with {habit_from_db}'

    def __my_input(self,message,history_file_name,commands):
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        print('Shelf Status   : ❌ Empty')
        return autocompleter.prompt_input(message,location=f"Home/UpdateHabit").lower()


    def run(self):
        command_functions = {
            'name':[
                    self.__habit_inputs.set_habit_name,
                    "Enter the habit name: "
                    ],
            'view habit to update':[
                self.__habit_inputs.set_session_duration,
                ''
            ],
            'start_datetime':[
                    self.__habit_inputs.set_start_datetime,
                    "Enter the habit datetime: "
                ],
            'duration':[
                self.__habit_inputs.set_session_duration,
                "Enter the habit session duration: "
            ],
            'save':[
                self.__habit_inputs.save,
                ""
            ]
        }
        while True:
            commands = list(command_functions.keys())
            history_file_name = 'add_habit'
            user_input = self.__my_input("Enter command: ",history_file_name,commands)
            
            match user_input:
                case 'esc':
                    break
                case 'clear':
                    clear_screen()
            
            if user_input not in commands:
                print('invalid input')
                continue
            
            func,message = command_functions[user_input]
            if message =='':
                display_message = func()
            else:
                display_message = func(message)