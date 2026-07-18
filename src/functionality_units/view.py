    # @retry_until_success
    # def sort_habits(self):
    #     commands = ['asc','desc']
    #     history_file_name = 'sort_results'
    #     if self.__habits==[]:
    #         return True, 'sorry there are no habits to sort'

    #     order = self.__my_input('Enter the way you want to sort habits: ',history_file_name,commands)
    #     # ********* start of common functions ************        
    #     did_run_common_func = ran_common_functions(order)
    #     message_to_display = find_message(order)
    #     if did_run_common_func==False:
    #         return True, message_to_display
    #     elif did_run_common_func==True:
    #         return False, message_to_display
    #     # ********** end of common functions ************
    #     if order not in commands:
    #         return False, f'\'{order}\' is not a valid input'
        
    #     return True,'hello'
    
    # @retry_until_success
    # def sort_by(self,message):
    #     commands = ['name','datetime','status','duration']
    #     history_file_name = 'sort_by'
    #     order_by = self.__my_input(message,history_file_name,commands)
    #     # ********* start of common functions ************        
    #     did_run_common_func = ran_common_functions(order_by)
    #     message_to_display = find_message(order_by)
    #     if did_run_common_func==False:
    #         return True, message_to_display
    #     elif did_run_common_func==True:
    #         return False, message_to_display
    #     # ********** end of common functions ************
    #     return True,'hello'

    # @retry_until_success
    # def sort_by_name(self):
    #     pass

    # @retry_until_success
    # def sort_by_time(self):
    #     pass

    # @retry_until_success
    # def sort_by_date(self):
    #     pass

    # @retry_until_success
    # def sort_by_datetime(self):
    #     pass

    # @retry_until_success
    # def sort_by_status(self):
        # pass
from rich.table import Table
from rich.console import Console

class View:

    def __init__(self):
        self.console = Console()
        self.__create_table()

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
        if final_index>max_len:
            final_index=max_len
            if final_index-initial_index<0:
                return initial_index-10,final_index

        if final_index-initial_index!=10:
            final_index=initial_index+10

        return initial_index,final_index

    def __back(self,initial_index,final_index):
        initial_index-=10
        final_index-=10
        if initial_index<0:
            initial_index = 0

        if final_index<10:
            final_index=10

        if final_index-initial_index!=10:
            final_index=initial_index+10
            
        return initial_index,final_index

    def display_habits(self,habits):
        max_len = len(habits)
        print(f'search results: {max_len}')
        initial_index = 0
        final_index = 10
        habits_to_display = habits[initial_index:final_index]
        while(True):
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
    ]
    x.display_habits(results)