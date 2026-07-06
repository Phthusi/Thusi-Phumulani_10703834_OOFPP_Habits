from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.history import FileHistory
from .read_json import read_json_files
from colorama import Fore, Style
from rich.progress import Progress

class ProgressBar:
    def __init__(self, number_of_fields):
        self.__advance = 1/number_of_fields *100
        self.__progress_percentage = 0

    def completion(self):
        with Progress() as progress:
            task = progress.add_task("Completing: ", total=100)
            progress.update(task, advance=self.__progress_percentage)

    def increase_progress_percentage(self,increase_by=0):
        if increase_by==0:
            self.__progress_percentage += self.__advance
            return
        self.__progress_percentage += increase_by
        self.__progress_percentage = min(self.__progress_percentage, 100)

class Form:
    def __init__(self, fields: dict[str, bool]):
        self.fields = fields

    def get_fields(self):
        return self.fields
    
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
    
    def get_session(self):
        return self.__session

    def prompt_input(self, message, commands=None,example=None,location='Home',field_status=None):
        prompt_string = f"[📍location] {location} "+Style.BRIGHT + f"> {Fore.MAGENTA + message}"
        if example!=None:
            prompt_string = f"{Fore.LIGHTBLACK_EX+ example}\n"+prompt_string
        if self.__has_status:
            status = field_status
            if status!=None:
                print(f"{Fore.LIGHTBLACK_EX}Status: {status}")
        return self.get_session().prompt(ANSI(prompt_string)).strip()
