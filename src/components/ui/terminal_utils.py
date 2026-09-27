import time
import functools
import os

call_history = []

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
            if len(call_history) >= 1:
                call_history.clear()
                print(message)
                input('Press Enter to continue')
            else:
                temporary_message(message)
            if success:
                return success,message
    return wrapper

def trace_call(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        message = ''
        success = ''
        if type(result) is not bool and len(result)==2:
            success,message = result
        else:
            success = result
            
        if not success:
            call_history.append(function.__name__)
            if message=='':
                return success
        return success,message
    return wrapper

def ran_common_functions(user_input,function=None):
    '''
    try to make the help function that will help the user to pick things up quick
    e.g use html to show gifs
    '''
    match user_input:
        case 'help':
            if function==None:
                print('to be written')
            else:
                function()
            return True
        case 'clear':
            clear_screen()
            return True
        case 'esc':
            return False
    return None

def find_message(message):
    match message:
        case 'esc':
            return 'escaping...'
        case 'clear':
            return 'clearing screen...'
        case 'help':
            return 'help function'
    return None

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
