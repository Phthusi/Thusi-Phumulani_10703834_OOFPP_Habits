import time
import functools
import os
from pathlib import Path

call_history = []

def clear_screen():
    """Clears the terminal screen depending on the host operating system."""
    os.system("cls" if os.name == "nt" else "clear")

def retry_until_success(function):
    """Decorator that repeatedly executes a CLI input function until it succeeds.

    Evaluates validation output, displays feedback messages, checks `call_history`
    tracking, and prompts for confirmation if validation failures occur.

    Args:
        function (callable): Method or function returning a tuple `(success, message)`.

    Returns:
        callable: Wrapped function executing the input retry loop.
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
    """Decorator that tracks validation failures in global call history.

    Monitors function return values and appends the function name to `call_history`
    if execution flags an unsuccessful result (`False`).

    Args:
        function (callable): Validation function returning a boolean or `(success, message)` tuple.

    Returns:
        callable: Wrapped function with trace logic.
    """
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

def ran_common_functions(user_input,history_file_name=None,message=None):
    """Executes shared CLI shortcut commands based on user input strings.

    Args:
        user_input (str): Input command string ('help', 'clear', or 'esc').
        function (callable, optional): Custom help function callback. Defaults to None.

    Returns:
        bool | None: True if 'help' or 'clear' was handled, False for 'esc', 
            or None if the command was not recognized.
    """
    match user_input:
        case 'help':
            if history_file_name==None:
                print('to be written')
            else:
                help(history_file_name)
            return True
        case 'clear':
            clear_screen()
            return True
        case 'esc':
            return False
    return None

def find_message(message):
    """Maps command keyword strings to status descriptive text.

    Args:
        message (str): Target command keyword ('esc', 'clear', or 'help').

    Returns:
        str | None: Description string associated with the command keyword, 
            or None if unknown.
    """
    match message:
        case 'esc':
            return 'escaping...'
        case 'clear':
            return 'clearing screen...'
        case 'help':
            return 'help function'
    return None

def temporary_message(message, duration=2):
    """Displays a transient inline message in the terminal that disappears after a delay.

    Prints the message to standard output, pauses execution for `duration` seconds,
    and clears the printed line by overwriting it with whitespace.

    Args:
        message (str): Text message to display.
        duration (int, optional): Duration in seconds to display the message. 
            Defaults to 2.
    """
    print(message, end="", flush=True)
    time.sleep(duration)
    print("\r" + " " * len(message) + "\r", end="", flush=True)


def help(history_file_name,target=None):
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_name = BASE_DIR / f"{history_file_name}/Readme.md"
    lines = []
    with open(file_name) as f:
        lines = f.readlines()

    line = '-'*100
    if target:
        try:
            start_target_index = lines.index(f'<!-- start-{target} -->\n')
            lines[start_target_index+1] = line+'\n'+lines[start_target_index+1].replace('## ','')+line+'\n'
            end_target_index = lines.index(f'<!-- end-{target} -->\n')
        except Exception:
            start_target_index = 0
            end_target_index = 0
        if start_target_index==end_target_index:
            print(f'Cannot find content to display\nplease ensure that you have things like this <!-- start-{target} --> in your readme file')
        input('Press enter to continue')
        return
    try:
        start_purpose_index = lines.index('<!-- start-purpose -->\n')
        lines[start_purpose_index+1] = line+'\n'+lines[start_purpose_index+1].replace('Purpose','').replace('## ','')+line+'\n'
        end_purpose_index = lines.index('<!-- end-purpose -->\n')
    except Exception:
        start_purpose_index = 0
        end_purpose_index = 0

    try:    
        start_high_level_view_index = lines.index('<!-- start-high-level-view -->\n')
        end_high_level_view_index = lines.index('<!-- end-high-level-view -->\n')
    except Exception:
        start_high_level_view_index = 0
        end_high_level_view_index = 0

    if end_high_level_view_index==start_high_level_view_index or start_purpose_index==end_purpose_index:
        print('Cannot find content to display\nplease ensure that you have things like this <!-- start-high-level-view --> in your readme file')
        input('Press enter to continue')
        return

    print(''.join(lines[start_purpose_index+1:end_purpose_index])
          .replace('*','')
          .replace('#','')
          .replace('[','')
          .replace(']','')
          .replace('(table-of-contents)','')
          .replace('â€”','->'))
    
    print(''.join(lines[start_high_level_view_index+1:end_high_level_view_index])
          .replace('*','')
          .replace('#','')
          .replace('[','')
          .replace(']','')
          .replace('(table-of-contents)','')
          .replace('â€”','->'))
    
    input('Press enter to continue')