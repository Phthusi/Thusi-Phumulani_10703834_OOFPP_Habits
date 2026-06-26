from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.history import FileHistory
from .read_json import read_json_files
from colorama import Fore, Style

class AutoCompleter:
    def __init__(self,history_file_name, commands=[]):
        self.__history = FileHistory(f"{history_file_name}.txt")
        self.__common_commands = read_json_files()['common_commands']
        self.__commands = [*commands,*self.__common_commands]
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)

    def get_completer(self):
        return FuzzyCompleter(WordCompleter(self.__commands, ignore_case=True))

    def get_commands(self):
        return self.__commands
    
    def set_commmands(self,commands):
        self.__commands = commands
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)
    
    def get_session(self):
        return self.__session

    def prompt_input(self, message, commands=None,example=None):
        prompt_string = Style.BRIGHT + f"> {Fore.MAGENTA + message} \n"
        if example!=None:
            prompt_string += f"{Fore.LIGHTBLACK_EX+ example}\n"
        return self.get_session().prompt(ANSI(prompt_string)).strip()
