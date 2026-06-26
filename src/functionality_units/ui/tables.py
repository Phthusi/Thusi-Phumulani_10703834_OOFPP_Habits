from rich.table import Table
from rich.console import Console

class MyTable:
    def __init__(self,name,column_names):
        self.__console = Console()
        self.__columns = column_names
        self.__table = Table(title=name)
        self.__add_columns()

    def __add_columns(self):
        for column in self.__columns:
            self.__table.add_column(column)

    def add_rows(self,data):
        for entry in data:
            self.__table.add_row(*entry)

    def display_table(self):
        self.__console.print(self.__table)    

if '__main__'== __name__:

    table = MyTable('Habit',['Id','Name','Start time','Duration','Status'])
    table.add_rows([
        ('1','Play Football','2022-02-11 15:00:00','00:15:00','UPCOMING'),
        ('2','Practice Football','2022-02-11 15:00:00','00:05:00','UPCOMING'),
        ('2','Practice Football','2022-02-11 15:00:00','00:05:00','UPCOMING'),
    ])

    table.display_table()