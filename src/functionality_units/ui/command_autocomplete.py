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

class AutoCompleter:
    def __init__(self,history_file_name, commands=[],number_of_fields=1):
        self.__history = FileHistory(f"{history_file_name}.txt")
        self.__common_commands = read_json_files()['common_commands']
        self.__commands = [*commands,*self.__common_commands]
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)
        self.__has_progress_bar = False
        self.__has_status = False
        self.__number_of_fields = number_of_fields
        self.__progress_bar = ProgressBar(number_of_fields)

    def get_completer(self):
        return FuzzyCompleter(WordCompleter(self.__commands, ignore_case=True))

    def get_commands(self):
        return self.__commands
    
    def set_commmands(self,commands):
        self.__commands = commands
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)
    
    def get_session(self):
        return self.__session

    def set_has_progress_bar(self,has_progress_bar):
        self.__has_progress_bar = has_progress_bar

    def set_has_status(self,has_status: bool):
        self.__has_status = has_status

    def prompt_input(self, message, commands=None,example=None,location='Home'):
        prompt_string = f"[📍location] {location} "+Style.BRIGHT + f"> {Fore.MAGENTA + message}"
        if example!=None:
            prompt_string += f"{Fore.LIGHTBLACK_EX+ example}"
        if self.__has_progress_bar:
            pass
        if self.__has_status:
            print('State of field: ❌ not filled')
        return self.get_session().prompt(ANSI(prompt_string)).strip()
