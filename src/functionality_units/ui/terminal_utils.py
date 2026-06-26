import time
import functools
import os

def clear_screen():
    """
    Clears the terminal screen depending on OS.
    """
    os.system("cls" if os.name == "nt" else "clear")

def retry_until_success(function):
    """
    Repeats a function call until it returns True.
    Intended for CLI input validation.
    """

    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        while True:
            success,message = function(self, *args, **kwargs)
            temporary_message(message)
            if success:
                return message
    return wrapper

def ran_common_functions(user_input,help_message='to be written'):
    match user_input:
        case 'help':
            print(help_message)
            return True
        case 'clear':
            clear_screen()
            return True
        case 'esc':
            return False
    return None

def retry_until_success_v2(function):
    """
    Repeats a function call until it returns True.
    Intended for CLI input validation.
    """

    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        while True:
            message,success,method = function(self, *args, **kwargs)
            if success:
                return method
    return wrapper

def temporary_message(message, duration=2):
    """
    Displays a temporary message for a specified duration.

    Parameters:
        message (str): Message to display
        duration (int): Duration in seconds to display the message
    """
    print(message, end="", flush=True)
    time.sleep(duration)
    print("\r" + " " * len(message) + "\r", end="", flush=True)
