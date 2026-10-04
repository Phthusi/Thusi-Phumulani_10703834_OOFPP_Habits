from rich.table import Table
from rich.console import Console

class MyTable:
    """Wrapper class for building and displaying formatted tables using Rich.

    Attributes:
        __console (Console): Rich console instance for terminal output.
        __columns (list[str]): List of column names.
        __table (Table): Underlying Rich Table instance.
    """
    def __init__(self,name,column_names):
        """Initializes the table with a title and column headers.

        Args:
            name (str): Title displayed at the top of the table.
            column_names (list[str]): Column header strings.
        """
        self.__console = Console()
        self.__columns = column_names
        self.__table = Table(title=name)
        self.__add_columns()

    def __add_columns(self):
        """Appends configured column names to the internal Rich Table instance."""
        for column in self.__columns:
            self.__table.add_column(column)

    def add_rows(self,data):
        """Adds multiple data rows to the table.

        Args:
            data (iterable[iterable[str]]): Collection of row tuples or lists 
                matching the number of configured columns.
        """
        for entry in data:
            self.__table.add_row(*entry)

    def display_table(self):
        """Renders and prints the formatted table to the terminal console."""
        self.__console.print(self.__table)    

if '__main__'== __name__:

    table = MyTable('Habit',['Id','Name','Start time','Duration','Status'])
    table.add_rows([
        ('1','Play Football','2022-02-11 15:00:00','00:15:00','UPCOMING'),
        ('2','Practice Football','2022-02-11 15:00:00','00:05:00','UPCOMING'),
        ('2','Practice Football','2022-02-11 15:00:00','00:05:00','UPCOMING'),
    ])

    table.display_table()