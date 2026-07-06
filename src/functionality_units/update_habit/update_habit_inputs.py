from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message
from ..ui.tables import MyTable
from ..habit_input import Habit_Inputs
from .update_habit_validator import UpdateHabitValidator
from ...data.db_manager import CompleteHabit, Habits, Habit

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class UpdateHabitInputs(Habit_Inputs):
    def __init__(self):
        self.__update_habit_validator = UpdateHabitValidator()
        self.__number_of_habit_fields = None
        self.__field_names  = []
        self.__habit_to_update = CompleteHabit()
        self.__is_habit_id_found = False
        self.__my_table = MyTable('Habit',['Id','Name','Start time','Duration'])
        self.__habits = Habits()
        self.__main_form = Form({field: False for field in ['id','number_of_habit_fields']})
        self.__fields_to_update_form = None
        self.__current_fields = dict()
        super().__init__(BASE_DIR)

    def __my_input(self,message,history_file_name,commands,field_status=None):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"Home/UpdateHabit/{modified_history_file_name}",field_status=field_status).lower()

    @retry_until_success
    def find_habit_id(self,message):
        # reset habit to habit we found
        commands = []
        history_file_name='find_habit_id'
        habit_id = self.__my_input(message,history_file_name,commands,field_status=self.__main_form.get_field_status('id'))
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_id)
        
        message_to_display = find_message(habit_id)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        try:
            habit_id = int(habit_id)
        except Exception as e:
            return False, e
               
        if not self.__habits.id_is_available(habit_id):
            return True, f'{habit_id} habit with Id does not exist'

        self.__is_habit_id_found = True
        habit = self.__habits.get_habit_by_id(habit_id)[0]
        id, name, start_datetime, duration, status = habit
        self.__current_fields = {
            'id':id,
            'name':name,
            'start_datetime':start_datetime,
            'duration':duration,
            'status':status
        }
        self.__my_table.add_rows(
            [(str(id),name,start_datetime,duration),]
        )
        self.__habit = CompleteHabit(name,duration,start_datetime,status,id)
        self.__main_form.set_field_status('id',True)
        return True, f'success'

    @retry_until_success
    def set_habit_field_number(self,message):
        if not self.__is_habit_id_found:
            return True, 'Find the habit first'
        commands = ['1','2','3']
        history_file_name = 'num_habit_fields'
        habit_field_number = self.__my_input(message,history_file_name,commands,field_status=self.__main_form.get_field_status('number_of_habit_fields'))
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field_number)
        message_to_display = find_message(habit_field_number)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        if not self.__update_habit_validator.is_valid_habit_field_number(habit_field_number):
            return False, f"{habit_field_number} is not an integer in the set "+'{1,2,3}'
        self.__number_of_habit_fields = int(habit_field_number)
        self.__main_form.set_field_status('number_of_habit_fields',True)
        return True, 'success..'

    @retry_until_success
    def view_habit(self,message):
        if not self.__is_habit_id_found:
            return True, 'Find the habit first'
        commands = ['no','yes']
        history_file_name = 'view_habit'
        want_to_view_habit = self.__my_input(message,history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(want_to_view_habit)
        message_to_display = find_message(want_to_view_habit)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        if want_to_view_habit not in commands:
            return False,f"'{want_to_view_habit}' is not in the given options,please press space to see you options"
        if want_to_view_habit=='yes':
            self.__my_table.display_table()
            return True,'success...'
        return True,'success...'

    @retry_until_success
    def __choose_fields_to_update(self,message):
        if self.__main_auto_completer.get_form()!=None:
            self.__main_auto_completer.get_form().reset_fields()
        if not self.__is_habit_id_found:
            return True, 'Find the habit first'
        
        if self.__number_of_habit_fields==None:
            return True, 'You cannot choose fields to update before successfully setting the habit field number'
        
        commands = ['name','start_datetime','duration']
        history_file_name = 'choose_fields_to_update'
        if int(self.__number_of_habit_fields)==3:
            self.__field_names.extend(['name','start_datetime','duration'])
            return True, 'ran common functions'
        
        habit_field = self.__my_input(message,history_file_name,commands)
        # ********* start of common functions ************        
        did_run_common_func = ran_common_functions(habit_field)
        message_to_display = find_message(habit_field)
        if did_run_common_func==False:
            return True, message_to_display
        elif did_run_common_func==True:
            return False, message_to_display
        # ********** end of common functions ************
        
        if not self.__update_habit_validator.is_field_name_valid(habit_field):
            return False, f'Invalid habit field, it must be one of the following:{'\n'.join(commands)}'

        self.__field_names.append(habit_field)
        # self.__main_auto_completer.add_field_to_form(habit_field)
        return True, 'success...'
    
    def choose_fields_to_update(self,message):
        count = 0
        while True:
            message_to_display = self.__choose_fields_to_update(message)
            if message_to_display!='success...':
                break
            count+=1
            if count == self.__number_of_habit_fields:
                break
        self.__fields_to_update_form = Form({field: False for field in self.__field_names})
        
        

    def set_fields_to_update(self):
        commands = {
            'name':[
                    self.set_habit_name,
                    "Enter the habit name you want this to be updated to: "
                    ],
            'start_datetime':[
                    self.set_start_datetime,
                    "Enter the habit datetime you want this to be updated to: "
                ],
            'duration':[
                self.set_session_duration,
                "Enter the habit session duration you want this to be updated to: "
            ]
        }

        for field_name in self.__field_names:
            func,message = commands[field_name]
            display_message = func(message)
    
    def update_field_dict(self):
        commands = {
            'name': self._Habit_Inputs__habit._Habit__name,
            'start_datetime': self._Habit_Inputs__habit._Habit__start_date,
            'duration':self._Habit_Inputs__habit._Habit__session_duration,
        }
        # update the complete habit
        field_dict = dict()
        self._Habit_Inputs__habit._Habit__id = self.__current_fields['id']
        self._Habit_Inputs__habit._Habit__status = self.__current_fields['status']
        for command_name in commands.keys():
            field = commands[command_name]
            field_dict.update({command_name:field})
        field_dict = {field_name:field_dict[field_name] for field_name in field_dict.keys() if field_dict[field_name]!='default'}
        return field_dict

    @retry_until_success
    def update(self):
        if not self.__is_habit_id_found:
            return True, 'Find the habit first'
        if self.__number_of_habit_fields==None:
            return True, 'Choose the number of fields first'
        success,message = self._Habit_Inputs__habit.update_habit(**self.update_field_dict())
        self.__main_form.reset_fields()
        return True,message
    