from colorama import Back, Fore
class Shelf:
    """Manages a single-item class-level cache for temporarily storing a habit.

    This class serves as an in-memory staging shelf allowing habit details
    to be transferred across different terminal menus or actions without
    requiring immediate database queries.

    Attributes:
        __habits_shelf (set): Class-level set holding at most one habit tuple.
    """
    __habits_shelf = set()

    @classmethod
    def preserve_habit(cls,habit):
        """Stores a habit tuple in the shelf cache, replacing any existing habit.

        Args:
            habit (tuple): A habit data tuple containing id, name, start datetime,
                duration, status, and periodicity.
        """
        cls.__habits_shelf = set()
        cls.__habits_shelf.add(habit)
        if len(cls.__habits_shelf)!=1:
            cls.__habits_shelf.pop(0)
    
    @classmethod
    def display_state(cls):
        """Returns a formatted status string indicating if the shelf is empty or holds a habit.

        Returns:
            str: Terminal-formatted string detailing current shelf status and contents.
        """
        return 'Shelf Status    : ❌ Empty' if len(cls.__habits_shelf)!=1 else f'Shelf Status    : ✅ Shelf has the follwing habit\n{cls.display_habit()}'

    @classmethod
    def display_habit(cls):
        """Formats and displays the properties of the habit currently stored on the shelf.

        Returns:
            str: Colorized string representation of the habit details and user notes.
        """
        id,name,start_datetime,duration,status,periodicity = list(cls.__habits_shelf)[0]
        return f'''
{Back.BLUE} Habit                                             {Back.RESET}
 id             :{id}
 name           :{name}
 start datetime :{start_datetime}
 duration       :{duration}
 status         :{status} 
 periodicity    :{periodicity}

 {Fore.RED}Note: You cannot modify a missed/completed habit,
 you can only view it.{Fore.RESET}
'''

    @classmethod
    def copy_last_place_habit(cls):
        """Retrieves the habit tuple currently stored on the shelf.

        Returns:
            tuple or None: The stored habit tuple if available; otherwise, None.
        """
        if len(list(cls.__habits_shelf))!=0:
            return list(cls.__habits_shelf)[0]
        return None
    
    @classmethod
    def empty_shelf(cls):
        """Clears all stored entries from the shelf cache."""
        try:
            cls.__habits_shelf.clear()
        except Exception as e:
            pass