from rich.table import Table
from rich.console import Console
from .ui.command_autocomplete import AutoCompleter
from pathlib import Path
from .ui.terminal_utils import clear_screen


BASE_DIR = Path(__file__).resolve().parent
class View:

    def __init__(self):
        self.console = Console()
        self.__create_table()
        self.__page_number = 1
        self.__current_index = 0
        self.__selected_habit = None

    def __create_table(self):
        self.table = Table(title="Habits")
        self.table.add_column(" ")
        self.table.add_column("Id")
        self.table.add_column("Name")
        self.table.add_column("start_datetime")
        self.table.add_column("duration")
        self.table.add_column("status")

    def __my_input(self,message,history_file_name,commands,field_pair=None,base='Home/SearchHabit/'):
        self.__main_auto_completer = AutoCompleter(BASE_DIR / f"view_history/{history_file_name}",commands)
        self.__main_auto_completer.set_has_status(True)
        modified_history_file_name = "".join(list(map(lambda word:word.capitalize(),history_file_name.split('_'))))
        return self.__main_auto_completer.prompt_input(message,location=f"{base}{modified_history_file_name}",field_pair=field_pair).lower()

    def add_to_table(self,habits,indices):
        for index,habit in zip(indices,habits):
            id,name,datetime,duration,status = list(map(str,habit))
            if index==self.__current_index:
                self.table.add_row('→',id,name,datetime,duration,status)
                continue
            self.table.add_row(' ',id,name,datetime,duration,status)

    def display_habit(self):
        self.console.print(self.table)
        self.__create_table()

    def __next(self,initial_index,final_index,max_len):
        final_index = final_index+10        
        initial_index += 10
        self.__page_number +=1
        self.__current_index += 10
        self.__current_index -= self.__current_index%10
        if final_index>=max_len:
            final_index=max_len
            if final_index-initial_index<=0:
                self.__page_number -=1
                self.__current_index -= 10
                return initial_index-10,final_index

        if final_index-initial_index!=10:
            final_index=initial_index+10

        return initial_index,final_index

    def __back(self,initial_index,final_index):
        initial_index-=10
        final_index-=10
        self.__page_number -=1
        self.__current_index -= 10
        self.__current_index -= self.__current_index%10

        if initial_index<0:
            initial_index = 0
            self.__page_number +=1
            self.__current_index += 10

        if final_index<10:
            final_index=10

        if final_index-initial_index!=10:
            final_index=initial_index+10

        return initial_index,final_index

    def select_functionality(self,habits):
        self.__selected_habit = habits[self.__current_index]

    def up(self,min_len):
        self.__current_index -= 1
        if self.__current_index<min_len:
            self.__current_index=min_len

    def down(self,max_len):
        self.__current_index += 1
        new_max_len = max_len if max_len<self.__page_number*10 -1 else self.__page_number*10 -1
        if self.__current_index > new_max_len:
            self.__current_index = new_max_len

        if new_max_len==max_len and self.__current_index >= new_max_len:
            self.__current_index = new_max_len-1

    def display_habits(self,habits,location_base):
        max_len = len(habits)
        if max_len==0:
            print('search results : 0')
            return
        print(f'\nsearch results : {max_len}')
        initial_index = 0
        final_index = 10
        habits_to_display = habits[initial_index:final_index]
        while(True):
            print(f'\n\npages : {self.__page_number} of {max_len//10 + 1 if max_len%10!=0 else max_len//10 + 0}')
            list_of_indices = list(range(initial_index,final_index))
            self.add_to_table(habits_to_display,list_of_indices)
            self.display_habit()
            commands =  ['up','down','select','next page','prev page','esc']
            history_file_name = 'view'
            x = self.__my_input('Enter : ',history_file_name,commands,base=location_base)
            match x:
                case 'next page':
                    initial_index,final_index = self.__next(initial_index,final_index,max_len)
                case 'prev page':
                    initial_index,final_index = self.__back(initial_index,final_index)
                case 'down':
                    self.down(max_len)
                case 'up':
                    self.up(list_of_indices[0])
                case 'select':
                    self.select_functionality(habits)
                    break
                case 'clear':
                    clear_screen()
                case 'esc':
                    break
                case default:
                    print(f'\'{x}\' is an invalid input')
            habits_to_display = habits[initial_index:final_index]
            clear_screen()

if '__main__'==__name__:
    x = View()
    results = [
    (1, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (2, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (3, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (4, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (5, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (6, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (7, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (8, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (9, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (10, 'jogging', '2026-06-01 14:00:00', '00:15:00', 'MISSED'), 
    (11, 'studying all day', '2026-06-01 14:10:00', '00:15:00', 'UPCOMING'), 
    (12, 'jogging', '2026-06-10 14:10:00', '00:15:00', 'UPCOMING'), 
    (13, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (14, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (15, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (16, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (17, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (18, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (19, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (20, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (21, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (22, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (23, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (24, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (25, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    (26, 'jogging', '2026-06-25 14:10:00', '00:15:00', 'UPCOMING'),
    ]
    x.display_habits(results)