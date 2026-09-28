from ..ui.command_autocomplete import AutoCompleter,Form
from ..ui.terminal_utils import ran_common_functions, retry_until_success, find_message
from ..habit_input import Habit_Inputs
from .update_habit_validator import UpdateHabitValidator
from ..shelf import Shelf
from ..view import View
from colorama import Fore
from ...data.db_manager import CompleteHabit,Habits
from ..ui.terminal_utils import clear_screen

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

class UpdateHabitInputs(Habit_Inputs):
    def __init__(self):
        self.__update_habit_validator = UpdateHabitValidator()
        self.__number_of_habit_fields = None
        self.__field_names  = []
        self.__is_habit_found_in_shelf = False
        self.__main_form = Form({field: False for field in ['id','number_of_habit_fields']})
        self.__display_map = """
[cyan]📌 LEVEL 1: PARAMETERS[/] [green]{name}[/] Name [blue] {start_datetime}[/] Start Datetime [green] {duration}[/] Duration  | [cyan]🔒 LEVEL 2: ACTION(S) [/] Complete update"""
        self.__display_form = Form({field: False for field in ['name','start_datetime','duration']},self.__display_map)
        self.__fiiled_form = Form({field: True for field in ['name','start_datetime','duration']},self.__display_map)
        self.__fields_to_update_form = None
        self.__selected_habit_tuple = None
        self.__current_fields = dict()
        super().__init__(BASE_DIR)
        self.__habit = None
        self.__view = View()
        self.__shelf = Shelf()
        self.__habits = Habits()
        self.__copied_habit_status = "No habit has been copied from the shelf, please copy the habit from the shelf"

    def __my_input(self,message,history_file_name,commands,field_pair=None):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"Home/UpdateHabit/{modified_history_file_name}",field_pair=field_pair).lower()

    def get_habit(self):
        return self.__habit

    def get_main_form(self):
        return self.__main_form

    def display_copied_habit(self):
        if self.__habit is None:
            print(f'''{Fore.LIGHTBLACK_EX}Status        : ❌ {self.__copied_habit_status}
Habit ID      : {Fore.LIGHTBLUE_EX}N/A''')
            return
        print(f'''{Fore.LIGHTBLACK_EX}Status        : ✅ {self.__copied_habit_status}
Habit ID      : {Fore.LIGHTGREEN_EX}{self.__habit._Habit__id}''')

    def collect_copied_habit(self):
        self.__selected_habit_tuple = Shelf.copy_last_place_habit()
        habit = {
            'id':int(self.__selected_habit_tuple[0]),
            'name':self.__selected_habit_tuple[1],
            'start_date':self.__selected_habit_tuple[2],
            'session_duration':self.__selected_habit_tuple[3],
            'status':self.__selected_habit_tuple[4]
            } if self.__selected_habit_tuple is not None else None
        habit = CompleteHabit(**habit) if not habit is None else None
        if habit is None:
            self.__copied_habit_status = 'No habit was found in the shelf, please copy the habit from the shelf'
            return self.__copied_habit_status
        
        self.__current_fields = {
            'id':int(self.__selected_habit_tuple[0]),
            'name':self.__selected_habit_tuple[1],
            'start_datetime':self.__selected_habit_tuple[2],
            'duration':self.__selected_habit_tuple[3],
            'status':self.__selected_habit_tuple[4]
        }
        self.__habit = habit
        self.__copied_habit_status = "Habit has been successfully copied from the shelf"
        self.__is_habit_found_in_shelf = True
        self.__main_form.set_field_status('id',True)
        return 'success...'

    @retry_until_success
    def __choose_fields_to_update(self,message):
        clear_screen()
        self.__field_names = []
        if not self.__is_habit_found_in_shelf:
            print('Please search for the habit you want to update and select it before you come to this step')
            input('Press Enter to continue')
            return True, ''
        
        commands = ['name','start_datetime','duration']
        history_file_name = 'choose_fields_to_update'
        
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

    def view_habit_to_update(self):
        if self.__selected_habit_tuple is None:
            print('No selected habit')
            return
        self.__view.draw_plain_table(self.__selected_habit_tuple)
        input('press enter to stop viewing this')

    def set_fields_to_update(self):
        habit = self.__habits.get_habit_by_id(self.__habit.get_id())[0]
        id,name,start_datetime,duration,status,periodicity = habit
        saved_name = self._Habit_Inputs__habit._Habit__name
        saved_start_datetime = self._Habit_Inputs__habit._Habit__start_date
        saved_duration = self._Habit_Inputs__habit._Habit__session_duration
        commands = {
            'name':[
                    lambda: self.set_habit_name("Enter the habit name you want this to be updated to: ",
                    form=self.__fiiled_form,name=name,
                    field_value= saved_name if saved_name!='default' else None, 
                    update_mode=True)
                    ],
            'view habit to update':[
                self.view_habit_to_update,
            ],
            'start_datetime':[
                    lambda : self.set_start_datetime("Enter the habit datetime you want this to be updated to: ",
                    form=self.__fiiled_form,
                    start_datetime=start_datetime,
                    field_value= saved_start_datetime if saved_start_datetime!='default' else None, 
                    update_mode=True
                    )
                ],
            'duration':[
                lambda : self.set_session_duration("Enter the habit session duration you want this to be updated to: ",
                form=self.__fiiled_form,
                duration=duration,
                field_value= saved_duration if saved_duration!='default' else None, 
                update_mode=True
                )
            ]
        }

        for field_name in set(self.__field_names):
            func = commands[field_name][0]
            display_message = func()

        for field_name in super().get_main_form().get_fields():
            if field_name in super().get_main_form().get_filled_fields():
                self.__display_form.set_field_status(field_name,True)
            elif field_name in self.__display_form.get_fields():
                self.__display_form.set_field_status(field_name,False)
                
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
        if not self.__is_habit_found_in_shelf:
            return True, 'Find the habit first or copy the habit from the shelf'

        if len(self.update_field_dict().keys())==0:
            return True, 'At least have one filled field'
        
        success,message = self._Habit_Inputs__habit.update_habit(**self.update_field_dict())
        habit = self.__habits.get_habit_by_id(self.__habit.get_id())[0]
        self.__shelf.preserve_habit(tuple(habit))
        self.__is_habit_found_in_shelf = False
        self.__number_of_habit_fields = None
        self.__field_names = []
        self.__selected_habit_tuple = None
        self.__current_fields = dict()
        self.__habit = None
        self.__copied_habit_status = "No habit has been copied from the shelf, please copy the habit from the shelf"
        self.__main_form.reset_fields()
        self.__display_form.reset_fields()
        return True,message
    
    def get_display_form(self):
        return self.__display_form
    
    def set_display_map(self,display_map):
        self.__display_map = display_map
# gimp