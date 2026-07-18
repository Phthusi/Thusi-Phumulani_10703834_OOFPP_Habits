from rich.table import Table
from rich.console import Console

class View:

    def __init__(self):
        self.console = Console()
        self.__create_table()
        self.__page_number = 1
    def __create_table(self):
        self.table = Table(title="Habits")
        self.table.add_column("Id")
        self.table.add_column("Name")
        self.table.add_column("start_datetime")
        self.table.add_column("duration")
        self.table.add_column("status")

    def add_to_table(self,habits):
        for habit in habits:
            id,name,datetime,duration,status = list(map(str,habit))
            self.table.add_row(id,name,datetime,duration,status)

    def display_habit(self):
        self.console.print(self.table)
        self.__create_table()

    def __next(self,initial_index,final_index,max_len):
        final_index = final_index+10        
        initial_index += 10
        self.__page_number +=1

        if final_index>max_len:
            final_index=max_len
            if final_index-initial_index<0:
                self.__page_number -=1
                return initial_index-10,final_index

        if final_index-initial_index!=10:
            final_index=initial_index+10

        return initial_index,final_index

    def __back(self,initial_index,final_index):
        initial_index-=10
        final_index-=10
        self.__page_number -=1
        
        if initial_index<0:
            initial_index = 0
            self.__page_number +=1

        if final_index<10:
            final_index=10

        if final_index-initial_index!=10:
            final_index=initial_index+10

        return initial_index,final_index

    def display_habits(self,habits):
        max_len = len(habits)
        print(f'search results : {max_len}')
        initial_index = 0
        final_index = 10
        habits_to_display = habits[initial_index:final_index]
        while(True):
            print(f'pages : {self.__page_number} of {max_len//10 + 1 if max_len%10!=0 else 0}')
            self.add_to_table(habits_to_display)
            self.display_habit()
            x = input('Enter x: ')
            match x:
                case 'next':
                    initial_index,final_index = self.__next(initial_index,final_index,max_len)
                case 'back':
                    initial_index,final_index = self.__back(initial_index,final_index)

                case 'quit':
                    break
                case default:
                    print(f'\'{x}\' is an invalid input')
            habits_to_display = habits[initial_index:final_index]


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
    ]
    x.display_habits(results)