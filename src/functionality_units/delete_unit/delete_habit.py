from ...data.db_manager import CompleteHabit, Habits
from ..ui.command_autocomplete import AutoCompleter
from ..ui.terminal_utils import ran_common_functions, retry_until_success

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class DeleteHabit:

    def __init__(self):
        self.__habit = CompleteHabit()
        self.__habits = Habits()
        
    def __set_habit_id(self,message):
        history_file_name='habit_id'
        commands = []
        autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        return autocompleter.prompt_input(message)
    
    def __find_habit(self,id):
        habit = self.__habits.get_habit_by_id(id)
        if len(habit)==1:
            return "success", habit[0] 
        elif len(habit)>1:
            return "data has been corrupted", None
        else:
            return "Habit not found!",None

    def __delete_habit(self,habit):
        id, name, start_datetime, duration, status = habit
        self.__habit.set_id(id)
        self.__habit.set_name(name)
        self.__habit.set_session_duration(duration)
        self.__habit.set_status(status)
        self.__habit.set_start_date(start_datetime)
        return self.__habit.delete_habit()
    
    @retry_until_success
    def __set_id_of_habit(self,message):
        habit_id = self.__set_habit_id(message)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_id)
        if did_run_common_func==False:
            return True, 'ran common functions'
        elif did_run_common_func==True:
            return False, 'switching'
        # ********** end of common functions ************

        try:
            assert '-' not in habit_id, f"{habit_id} must be postive"
            assert '.' not in habit_id, f"{habit_id} must be a whole number"
            self.__habit.set_id(int(habit_id))
            return True, 'valid habit id'
        except Exception as e:
            return False,'Id must be an integer'
    
    def delete(self,message):
        message = self.__set_id_of_habit(message)
        if message !='valid habit id':
            return message
        
        id = self.__habit.get_id()
        message, habit = self.__find_habit(id)
        if habit==None:
            return message
        message,_ = self.__delete_habit(habit)
        return message