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
from src.components.time_project.time_manager import HabitDateTimeManager
from .read_json import read_json_files
from colorama import Fore, Style, Back
from ..shelf import Shelf

'''
update functionality FOR WEEKS
update functionality FOR MONTHS
'''

shelf = Shelf()

def update_habit_statuses():
    """Synchronizes stored habit statuses with real-time temporal constraints.

    Evaluates active habits stored in the database (excluding terminal statuses
    such as 'MISSED', 'UNKNOWN', and 'COMPLETED'), recalculates their status using
    HabitDateTimeManager, and updates both database storage and the local active
    habit cache when state changes occur.
    """
    db_interface = DB_Interface()
    habits = Habits()
    saved_habits = habits.get_habit_by_status_excluding_some_statuses(['MISSED','UNKNOWN','COMPLETED'])
    habit_datetime_manager = HabitDateTimeManager()
    update_cache = False
    for habit in saved_habits:
        id, name, start_datetime, duration, status, periodicity = habit
        new_status = habit_datetime_manager.determine_habit_status(start_datetime,duration)
        if new_status!=status:
            db_interface.update_habit(id,**{'status':new_status}) 
            update_cache = True
            copied_habit = shelf.copy_last_place_habit()
            copied_habit_id = -1 if copied_habit is None else copied_habit[0]
            db_interface.set_is_db_updated(True)
            if  copied_habit_id == id : 
                shelf.preserve_habit((id,name,start_datetime,duration,new_status,periodicity))
                
    if update_cache:
        db_interface.get_all_habits()
        update_cache = False

def display_urget_updates(location):
    """Displays urgent habit notifications based on user location in the CLI workflow.

    Queries the database for habits marked as 'TO_BE_CONFIRMED' and prints a styled
    warning banner to the terminal if pending items require action.

    Args:
        location (str): Current navigation context/location identifier (e.g., 'Home').
    """
    habits = Habits()
    habit_to_complete = habits.get_habit_by_status('TO_BE_CONFIRMED')
    locations_for_decos = ['Home']
    if len(habit_to_complete) >0:
        message = f'Notifications   : ⚠ You have {len(habit_to_complete)} habits to complete, Please search for habits to complete to complete these'
        if location in locations_for_decos:
            print(Fore.WHITE+f'''----------------------------------------------------------------------------------------------------------
{message}
----------------------------------------------------------------------------------------------------------''')
        else:
            print(f'''\n{Back.LIGHTBLACK_EX}                                                                                                         
  {message.replace('Notifications   : ',"").replace('You','').replace('⚠',Fore.YELLOW+'⚠'+Fore.WHITE)+' '}                  
                                                                                                         ''')
            Fore.RESET
            Style.RESET_ALL
class ProgressBar:
    """Renders terminal progress indicators using Rich panels and progress widgets.

    Manages a step-based progress metric for complex interactive flows such as
    query construction or multi-step form entry.
    """
    def __init__(self, number_of_fields):
        self.__advance = 1/number_of_fields *100
        self.__progress_percentage = 0

    def display_progress_bar(self,menu_text="to be"):
        """Renders an animated panel containing the current progress state.

        Args:
            menu_text (str, optional): Descriptive text or menu markup to embed 
                inside the query builder panel. Defaults to "to be".
        """
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
        """Increments the progress percentage up to a maximum cap of 95%.

        Args:
            increase_by (int, optional): Number of field completion units to increment. Defaults to 0.
        """
        if increase_by==0:
            return
        self.__progress_percentage += increase_by * self.__advance
        self.__progress_percentage = min(self.__progress_percentage, 95)

    def complete_progress(self):
        """Forces the progress percentage indicator to 100% completion."""
        self.__progress_percentage = 100

class Form:
    """Manages multi-field data entry state and formatting mapping for forms.

    Tracks completion status for named input fields and produces formatted string 
    representations featuring visual status icons (✅/❌).
    """
    def __init__(self, fields: dict[str, bool],display_map=None,levels=None):
        """Initializes the form tracking structure.

        Args:
            fields (dict[str, bool]): Mapping of field names to initial completion boolean states.
            display_map (str, optional): Template format string for displaying form status. Defaults to None.
            levels (dict, optional): Additional contextual metadata mapping used during format formatting. Defaults to None.
        """
        self.fields = fields
        self.__display_map = display_map
        self.__levels = levels

    def get_fields(self):
        """Returns the current field completion status dictionary.

        Returns:
            dict[str, bool]: Key-value pair of field names and their completion status.
        """
        return self.fields
    
    def set_map(self,map_string):
        """Sets the raw mapping template string.

        Args:
            map_string (str): Template string for the form map.
        """
        self.__map_string = map_string

    def set_display_map(self,display_map):
        """Sets the template format string for human-readable output display.

        Args:
            display_map (str): Display template string containing `{field_name}` placeholders.
        """
        self.__display_map = display_map

    def get_raw_map(self):
        """Retrieves the unformatted display template map string.

        Returns:
            str: Raw display template string.
        """
        return self.__display_map

    def get_display_map(self):
        """Formats the display map string, substituting boolean values with visual status indicators.

        Returns:
            str: Interpolated string representation replacing `True` with '✅' and `False` with '❌'.
        """
        if self.__levels:
            fields = self.fields.copy()
            fields.update(self.__levels)
            return self.__display_map.format(**fields).replace('True','✅').replace('False','❌')
        return self.__display_map.format(**self.fields).replace('True','✅').replace('False','❌')

    def set_fields(self, fields):
        """Replaces the active form fields mapping.

        Args:
            fields (dict[str, bool]): New dictionary mapping of field names to boolean statuses.
        """
        self.fields = fields

    def add_field(self, field_name):
        """Registers a new input field into the form initialized as uncompleted (`False`).

        Args:
            field_name (str): Name of the new field to track.
        """
        if field_name not in self.fields:
            self.fields[field_name] = False

    def field_filled(self, field_name):
        """Marks a specific field as completed (`True`).

        Args:
            field_name (str): Name of the field to update.
        """
        if field_name in self.fields:
            self.fields[field_name] = True

    def is_filled(self, field_name):
        """Checks whether a given field has been filled.

        Args:
            field_name (str): Name of the field to check.

        Returns:
            bool: True if filled, False if unfilled or non-existent.
        """
        return self.fields.get(field_name, False)
    
    def number_of_filled_fields(self):
        """Counts the total number of fields marked as filled.

        Returns:
            int: Number of completed form fields.
        """
        return sum(1 for filled in self.fields.values() if filled)

    def get_field_status(self, field_name,field_value=None,update_mode=False):
        """Generates a status summary string for a given field.

        Args:
            field_name (str): Name of the field to evaluate.
            field_value (Any, optional): Value assigned to the field in update contexts. Defaults to None.
            update_mode (bool, optional): Whether to format output for update mode operations. Defaults to False.

        Returns:
            str | None: Formatted status message describing field completion and value,
                or None if `field_name` is None.
        """
        additional_message = ''
        if update_mode and field_value is None:
            additional_message = f'{field_name} to be update to: N/A\n'
        elif update_mode:
            additional_message = f'{field_name} to be update to: {field_value}\n'
        if field_name in self.fields:
            return additional_message + f"✅ {field_name} filled" if self.fields[field_name] else f"❌ {field_name} not filled"
        if field_name is None:
            return None
        return f"{field_name} not found"
    
    def all_fields_filled(self):
        """Determines if every tracked field in the form is marked as completed.

        Returns:
            bool: True if all fields are True, False otherwise.
        """
        return all(self.fields.values())
    
    def reset_fields(self):
        """Resets all tracked fields in the form to uncompleted (`False`)."""
        for field in self.fields:
            self.fields[field] = False

    def get_filled_fields(self):
        """Retrieves a list of all field names currently marked as completed.

        Returns:
            list[str]: List of field names where status is True.
        """
        return [field for field, filled in self.fields.items() if filled]
    
    def get_unfilled_fields(self):
        """Retrieves a list of all field names currently marked as incomplete.

        Returns:
            list[str]: List of field names where status is False.
        """
        return [field for field, filled in self.fields.items() if not filled]

    def set_field_status(self, field_name, status):
        """Explicitly sets the boolean completion state for a target field.

        Args:
            field_name (str): Name of the field to update.
            status (bool): Completion status to set.
        """
        if field_name in self.fields:
            self.fields[field_name] = status

class AutoCompleter:
    """Manages command-line prompt sessions with persistent history and fuzzy autocompletion.

    Wraps prompt_toolkit's PromptSession with common application commands, status updates,
    and urgent habit reminders.
    """
    def __init__(self,history_file_name, commands=[]):
        """Initializes the autocompleter with persistent history file and command sets.

        Args:
            history_file_name (str): Base filename (without extension) for loading and saving prompt history.
            commands (list[str], optional): Additional custom commands to combine with default common commands. Defaults to [].
        """
        self.__history = FileHistory(f"{history_file_name}.txt")
        self.__common_commands = read_json_files()['common_commands']
        self.__commands = [*commands,*self.__common_commands]
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)
        self.__has_status = False

    def get_completer(self):
        """Constructs a FuzzyCompleter wrapping a WordCompleter for registered commands.

        Returns:
            FuzzyCompleter: Case-insensitive fuzzy matching completion engine.
        """
        return FuzzyCompleter(WordCompleter(self.__commands, ignore_case=True))

    def get_commands(self):
        """Retrieves the full list of autocomplete commands available in the session.

        Returns:
            list[str]: Registered prompt commands.
        """
        return self.__commands
    
    def add_field_to_form(self, field_name):
        """Adds a field entry to an internal form instance if present.

        Args:
            field_name (str): Name of the field to append.
        """
        self.__form.add_field(field_name)
    
    def set_commmands(self,commands):
        """Replaces the current active commands list and reinitializes the prompt session.

        Args:
            commands (list[str]): New list of command strings to enable for completion.
        """
        self.__commands = commands
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)

    def set_has_status(self, has_status):
        """Configures whether field status and value summaries should print during prompting.

        Args:
            has_status (bool): True to render field status block prior to prompt entry.
        """
        self.__has_status = has_status
    
    def set_has_progress_bar(self, has_progress_bar):
        """Configures progress bar display settings for prompt interactions.

        Args:
            has_progress_bar (bool): True to enable progress bar UI context.
        """
        self.__has_progress_bar = has_progress_bar

    def get_session(self):
        """Returns the underlying prompt_toolkit PromptSession instance.

        Returns:
            PromptSession: Active command prompt session.
        """
        return self.__session

    def prompt_input(self, message, commands=None,example=None,location='Home',field_pair=None,multiple_values=""):
        """Displays notifications, optional field status metadata, and captures user terminal input.

        Triggers habit status updates, renders urgent notification banners, formats location-aware
        prompts, and prompts the user via the active PromptSession.

        Args:
            message (str): Prompt text presented to the user.
            commands (list[str], optional): Unused override parameter for prospective command sets. Defaults to None.
            example (str, optional): Optional helper guide or keyboard shortcut reference string. Defaults to None.
            location (str, optional): Current active navigation scope string. Defaults to 'Home'.
            field_pair (tuple[str, Any], optional): Tuple containing (field_status, field_value) for active metadata tracking. Defaults to None.
            multiple_values (str, optional): Additional text appended to the current field value line. Defaults to "".

        Returns:
            str: Striped string containing input entered by the user.
        """
        update_habit_statuses()
        display_urget_updates(location)
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
                if '\n' in status:
                    additional_message,status = status.split('\n')
                    print(f"""{Fore.LIGHTBLACK_EX}{additional_message}""")
                print(f"""{Fore.LIGHTBLACK_EX}Status        : {status}
Current Value : {Fore.LIGHTBLUE_EX if field_value is None else Fore.LIGHTGREEN_EX}{field_value if field_value is not None else 'N/A'}{Fore.LIGHTBLACK_EX + multiple_values}{Fore.RESET}""")
        return self.get_session().prompt(ANSI(prompt_string)).strip()
