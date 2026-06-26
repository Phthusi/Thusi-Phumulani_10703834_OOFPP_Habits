# from ...data.db_manager import CompleteHabit, Habits, DB_Interface
# from ..ui.command_autocomplete import AutoCompleter
# from ..time_project.time_manager import HabitDateTimeManager
# from ..ui.terminal_utils import ran_common_functions, retry_until_success
# from .update_habit_validator import UpdateHabitValidator
# from ..time_project.time_manager_validator import HabitDateTimeManagerValidator

# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent

# class UpdateHabit:

#     def __init__(self):
#         self.__habit = CompleteHabit()
#         self.__update_habit_validator = UpdateHabitValidator()
#         self.__habit_datetime_manager_validator = HabitDateTimeManagerValidator()
#         self.__habits = Habits()
#         self.__habit_fields = {}
#         self.__number_of_habit_fields = None
#         self.__field_values = []
#         self.__field_names  = []

#     # non-update functions
#     def __add_field(self,field_name):
#         self.__field_names.append(field_name)

#     def __remove_field(self):
#         return self.__field_names.pop()

#     def __add_field_value(self,field_value):
#         self.__field_values.append(field_value)

#     def __remove_value(self):
#         return self.__field_names.pop()

#     def __set_num_of_habit_habit_fields(self,message):
#         history_file_name = 'num_habit_fields'
#         commands = ['1','2','3']
#         autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
#         return autocompleter.prompt_input(message)

#     @retry_until_success
#     def set_habit_field_number(self,message):
#         habit_field_number = self.__set_num_of_habit_habit_fields(message)
#         if not self.__update_habit_validator.is_valid_habit_field_number(habit_field_number):
#             return False, f"{habit_field_number} is not an integer between 1 and 3"
#         self.__number_of_habit_fields = habit_field_number
#         return True, 'success..'

#     def __set_habit_habit_field(self,message):
#         history_file_name='habit_fields'
#         commands = ['name','start_datetime','duration']
#         autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
#         return autocompleter.prompt_input(message)

#     def is_duration_valid(self,duration):
#         return self.__habit_datetime_manager_validator.is_time_format_valid(duration)

#     def is_date_valid(self,datetime):
#         is_time_valid = self.__habit_datetime_manager_validator.is_date_valid(datetime)
#         is_time_passed = False
#         if is_time_valid:
#             is_time_passed = self.__habit_datetime_manager_validator.is_passed(datetime)
#             if is_time_passed:
#                 return False, f'{datetime} has passed'
#             return True, f'{datetime} is valid'
#         return False, f'{datetime} has an invalid format'
    
#     def __set_name(self):
#         history_file_name='habit_name'
#         commands = []
#         autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
#         return autocompleter.prompt_input('Enter the name of the habit')

#     def __set_start_datetime(self):
#         history_file_name='start_datetime'
#         commands = []
#         autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
#         return autocompleter.prompt_input('Enter the start datetime of the habit')

#     def __set_duration(self):
#         history_file_name='start_datetime'
#         commands = []
#         autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
#         return autocompleter.prompt_input('Enter the habit duration of the habit')

#     @retry_until_success
#     def __update_habit_duration(self):
#         duration = self.__set_duration()
#         # ********* start of common functions ************        
#         did_run_common_func = ran_common_functions(duration)
#         if did_run_common_func==False: 
#             return True, 'ran common functions'
#         elif did_run_common_func==True:
#             return False, 'switching'
#         # ********** end of common functions ************
#         if self.is_duration_valid(duration):
#             # set habit field
#             self.__remove_field()
#             return True, 'success..'
#         return False,'duration is invalid'

#     def set_field_val_unit(self):
#         '''
#         get field
#         get value
#         join them
#         '''
#         pass

#     @retry_until_success
#     def __set_habit_field(self,message):
#         '''
#         get habit field name
#         validate it
#         get habit field value
#         validate it
#         match habit field name with
#         '''
#         habit_field = self.__set_habit_habit_field(message).lower()
#         # ********* start of common functions ************        
#         did_run_common_func = ran_common_functions(habit_field)
#         if did_run_common_func==False:
#             return True, 'ran common functions'
#         elif did_run_common_func==True:
#             return False, 'switching'
#         # ********** end of common functions ************
#         if not self.__update_habit_validator.is_field_name_valid(habit_field):
#             return False,f'{habit_field} is not found in the following options name,start_datetime and duration'

#         fields = {
#             'name':{
#                 'validator':self.__update_habit_validator.is_name_valid,
#                 'set':self.__set_name
#                 },
#             'start_datetime':{
#                 'validator':self.is_date_valid,
#                 'set':self.__set_start_datetime
#                 },
#             'duration':{
#                 'validator':self.is_duration_valid,
#                 'set':self.__set_duration
#                 }
#         }
        
#         field = retry_until_success(fields.get(habit_field)['set'])
#         if field==None:
#             print('what!')
#         success, message = fields.get(habit_field)['validator'](field)
        
#         return True,'success...'

#     def __set_habit_id(self,message):
#         history_file_name='habit_id'
#         commands = []
#         autocompleter = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
#         return autocompleter.prompt_input(message)
    
#     def __find_habit(self,id):
#         habit = self.__habits.get_habit_by_id(id)
#         if len(habit)==1:
#             return "success", habit[0] 
#         elif len(habit)>1:
#             return "data has been corrupted", None
#         else:
#             return "Habit not found!",None

#     def __update_habit(self,habit,**kwargs):
#         id, name, start_datetime, duration, status = habit
#         self.__habit.set_id(id)
#         self.__habit.set_name(name)
#         self.__habit.set_session_duration(duration)
#         self.__habit.set_status(status)
#         self.__habit.set_start_date(start_datetime)
#         return self.__habit.update_habit(**kwargs)

#     @retry_until_success
#     def __set_habit_value(self,message):
#         habit_field = self.__set_habit_habit_fields(message)
#         # ********* start of common functions ************        
#         did_run_common_func = ran_common_functions(habit_field)
#         if did_run_common_func==False:
#             return True, 'ran common functions'
#         elif did_run_common_func==True:
#             return False, 'switching'
#         # ********** end of common functions ************

#     @retry_until_success
#     def __set_id_of_habit(self,message):
#         habit_id = self.__set_habit_id(message)
#         # ********* start of common functions ************        
#         did_run_common_func = ran_common_functions(habit_id)
#         if did_run_common_func==False: 
#             return True, 'ran common functions'
#         elif did_run_common_func==True:
#             return False, 'switching'
#         # ********** end of common functions ************
#         success, message = self.__update_habit_validator.is_valid_id(habit_id)            
#         if success:
#             self.__habit.set_id(habit_id)
#         return success, message

#     def update(self,message):
#         message = self.__set_id_of_habit(message)
#         if message !='valid habit id':
#             return message
        
#         id = self.__habit.get_id()
#         message, habit = self.__find_habit(id)
#         if habit==None:
#             return message
#         # habit fields 
#         success, message = self.__update_habit(habit,**kwargs)
#         return message

#     def complete_session(self,message):
#         id = self.__set_id_of_habit(message)
#         message, habit = self.__find_habit(id)
#         if message=='error':
#             return message
        
#         self.__habit.set_status("COMPLETED")
#         success, message = self.__update_habit(habit)
#         return message

#     def update_statuses():
#         db_interface = DB_Interface()
#         habits = Habits()

#         saved_habits = habits.get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])
#         habit_datetime_manager = HabitDateTimeManager()
#         for habit in saved_habits:
#             id, _, start_datetime, duration, status = habit
#             new_status = habit_datetime_manager.determine_habit_status(start_datetime,duration)
#             if new_status!=status:
#                 db_interface.update_habit(id,**{'status':new_status}) 
