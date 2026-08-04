from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.history import FileHistory
from src.data.db_functionality.db_interface import DB_Interface
from src.data.db_manager import Habits
from src.functionality_units.time_project.time_manager import HabitDateTimeManager
from .read_json import read_json_files
from colorama import Fore, Style


def update_habit_statuses():
    db_interface = DB_Interface()
    habits = Habits()
    saved_habits = habits.get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN'])
    habit_datetime_manager = HabitDateTimeManager()
    for habit in saved_habits:
        id, name, start_datetime, duration, status = habit
        new_status = habit_datetime_manager.determine_habit_status(start_datetime,duration)
        if new_status!=status:
            db_interface.update_habit(id,**{'status':new_status}) 
class ProgressBar:
    def __init__(self, number_of_fields):
        self.__advance = 1/number_of_fields *100
        self.__progress_percentage = 0

    def display_progress_bar(self,menu_text="to be"):
        progress = Progress(
            TextColumn("[bold magenta]Complete        :[/]"),
            BarColumn(
                complete_style="blue",
                finished_style="bright_white",
                style="on rgb(40,40,40)",
            ),
            TextColumn("[white]{task.percentage:>3.0f}%"),
        )
        task = progress.add_task("", total=100)
        progress.update(task, completed=self.__progress_percentage)

        ui_content = Group(progress, menu_text)
        ui_panel = Panel(
            ui_content,
            title="[bold]🧭 QUERY BUILDER[/]",
            title_align="center",
            border_style="bright_white",
            padding=(1, 2),
            expand=True,
        )

        with Live(ui_panel, refresh_per_second=4):
            pass

    def increase_progress_percentage(self,increase_by=0):
        if increase_by==0:
            return
        self.__progress_percentage += increase_by * self.__advance
        self.__progress_percentage = min(self.__progress_percentage, 95)

    def complete_progress(self):
        self.__progress_percentage = 100

class Form:
    def __init__(self, fields: dict[str, bool],display_map=None):
        self.fields = fields
        self.__display_map = display_map
 
    def get_fields(self):
        return self.fields
    
    def set_map(self,map_string):
        self.__map_string = map_string

    def set_display_map(self,display_map):
        self.__display_map = display_map

    def get_display_map(self):
        return self.__display_map.format(**self.fields).replace('True','✅').replace('False','❌')

    def set_fields(self, fields):
        self.fields = fields

    def add_field(self, field_name):
        if field_name not in self.fields:
            self.fields[field_name] = False

    def field_filled(self, field_name):
        if field_name in self.fields:
            self.fields[field_name] = True

    def is_filled(self, field_name):
        return self.fields.get(field_name, False)
    
    def number_of_filled_fields(self):
        return sum(1 for filled in self.fields.values() if filled)

    def get_field_status(self, field_name):
        if field_name in self.fields:
            return f"✅ {field_name} filled" if self.fields[field_name] else f"❌ {field_name} not filled"
        if field_name is None:
            return None
        return f"{field_name} not found"
    
    def all_fields_filled(self):
        return all(self.fields.values())
    
    def reset_fields(self):
        for field in self.fields:
            self.fields[field] = False
    
    def get_filled_fields(self):
        return [field for field, filled in self.fields.items() if filled]
    
    def get_unfilled_fields(self):
        return [field for field, filled in self.fields.items() if not filled]

    def set_field_status(self, field_name, status):
        if field_name in self.fields:
            self.fields[field_name] = status

class AutoCompleter:
    def __init__(self,history_file_name, commands=[]):
        self.__history = FileHistory(f"{history_file_name}.txt")
        self.__common_commands = read_json_files()['common_commands']
        self.__commands = [*commands,*self.__common_commands]
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)
        self.__has_status = False

    def get_completer(self):
        return FuzzyCompleter(WordCompleter(self.__commands, ignore_case=True))

    def get_commands(self):
        return self.__commands
    
    def add_field_to_form(self, field_name):
        self.__form.add_field(field_name)
    
    def set_commmands(self,commands):
        self.__commands = commands
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)

    def set_has_status(self, has_status):
        self.__has_status = has_status
    
    def set_has_progress_bar(self, has_progress_bar):
        self.__has_progress_bar = has_progress_bar

    def get_session(self):
        return self.__session

    def prompt_input(self, message, commands=None,example=None,location='Home',field_pair=None):
        update_habit_statuses()
        if field_pair is None:
            field_status=None
            field_value=None
        else:
            field_status,field_value = field_pair
            field_value = None if field_value=='default' else field_value
        prompt_string = f"[📍location] {location} "+Style.BRIGHT + f"> {Fore.MAGENTA + message}"
        if example!=None:
            prompt_string = f"{Fore.LIGHTBLACK_EX+ example}\n{Fore.WHITE}"+prompt_string
        
        if self.__has_status:
            status = field_status
            if status!=None:
                print(f"""{Fore.LIGHTBLACK_EX}Status        : {status}
Current Value : {Fore.LIGHTBLUE_EX if field_value is None else Fore.LIGHTGREEN_EX}{field_value if field_value is not None else 'N/A'}{Fore.RESET}""")
        return self.get_session().prompt(ANSI(prompt_string)).strip()
