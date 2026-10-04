from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent


class WeekPattern:
    """Represents a single named week pattern containing active weekdays.

    Attributes:
        week_patterns (dict[str, list[str]]): Class-level registry mapping pattern 
            names to lists of active weekday strings.

    Example:
        >>> wp = WeekPattern('workdays')
        >>> wp.set_week_pattern(['mon', 'tue', 'wed', 'thu', 'fri'])
        >>> print(wp)
        week_name: workdays
        MON
        TUE
        WED
        THU
        FRI
    """
    week_patterns = dict()
    def __init__(self,name):
        """Initializes a new WeekPattern instance.

        Args:
            name (str): The unique identifier for this week pattern.

        Example:
            >>> wp = WeekPattern('weekend')
        """
        self.__name = name
        self.__week_pattern = []

    def set_week_pattern(self,week_pattern):
        """Sets the active list of weekdays for this pattern.

        Args:
            week_pattern (list[str]): List of short weekday names (e.g., ['mon', 'fri']).

        Example:
            >>> wp = WeekPattern('gym_days')
            >>> wp.set_week_pattern(['mon', 'wed', 'fri'])
        """
        self.__week_pattern = week_pattern

    def get_week_pattern(self):
        """Retrieves the list of active weekdays in this pattern.

        Returns:
            list[str]: Active weekday strings assigned to this pattern.

        Example:
            >>> wp.get_week_pattern()
            ['mon', 'wed', 'fri']
        """
        return self.__week_pattern
    
    def get_name(self):
        """Retrieves the name of this week pattern.

        Returns:
            str: The unique pattern name.

        Example:
            >>> wp.get_name()
            'gym_days'
        """
        return self.__name
    
    def set_name(self,name):
        """Updates the name of this week pattern.

        Args:
            name (str): The new unique identifier for the pattern.

        Example:
            >>> wp.set_name('workout_routine')
        """
        self.__name = name
        
    def __repr__(self):
        """Returns a string representation of the week pattern.

        Returns:
            str: Formatted pattern name and uppercase list of active weekdays.

        Example:
            >>> repr(wp)
            'week_name: workout_routine\\n MON\\n WED\\n FRI'
        """
        return f"week_name: {self.get_name()}{'\n '.join(list(map(lambda day: day.upper(),self.get_week_pattern())))}"

class WeekPatternManager:
    """Manages creation, updates, lookup, and deletion of `WeekPattern` instances.

    Example:
        >>> manager = WeekPatternManager()
        >>> manager.save_week_pattern('week1', ['mon', 'tue'])
        (True, 'week pattern saved successfully')
    """
    def find_week_pattern(self,name):
        """Finds a saved week pattern by name.

        Args:
            name (str): The name of the week pattern to retrieve.

        Returns:
            list[str] | None: List of active weekdays if found, otherwise None.

        Example:
            >>> manager.find_week_pattern('week1')
            ['mon', 'tue']
        """
        return WeekPattern.week_patterns.get(name,None)
    
    def get_saved_weeks(self):
        """Retrieves all registered week patterns.

        Returns:
            dict[str, list[str]]: Dictionary mapping week pattern names to active weekday lists.

        Example:
            >>> manager.get_saved_weeks()
            {'week1': ['mon', 'tue']}
        """
        return WeekPattern.week_patterns
    
    def delete_week_pattern(self,name):
        """Removes a saved week pattern from the registry.

        Args:
            name (str): The name of the week pattern to remove.

        Returns:
            list[str] | None: The removed weekday list if found, otherwise None.

        Example:
            >>> manager.delete_week_pattern('week1')
            ['mon', 'tue']
        """
        WeekPattern.week_patterns.pop(name,None)

    def update_week_pattern(self,name,week_pattern):
        """Updates an existing week pattern in the registry.

        Args:
            name (str): Name of the week pattern to update.
            week_pattern (list[str]): New list of active weekdays.

        Example:
            >>> manager.update_week_pattern('week1', ['mon', 'wed', 'fri'])
        """
        if name in WeekPattern.week_patterns:
            WeekPattern.week_patterns[name] = week_pattern

    def save_week_pattern(self,name,week_pattern):
        """Saves a new week pattern to the registry if the name is unique.

        Args:
            name (str): Unique name for the new week pattern.
            week_pattern (list[str]): List of active weekday strings.

        Returns:
            tuple[bool, str]: A tuple containing success boolean and status message.

        Example:
            >>> manager.save_week_pattern('week2', ['sat', 'sun'])
            (True, 'week pattern saved successfully')
            >>> manager.save_week_pattern('week2', ['mon'])
            (False, "Sorry new week pattern with name 'week2' already exists")
        """
        if name not in WeekPattern.week_patterns:
            WeekPattern.week_patterns[name] = week_pattern
            return True,'week pattern saved successfully'
        return False, f'Sorry new week pattern with name \'{name}\' already exists'

    @classmethod   
    def clear(cls):
        """Clears all saved week patterns from class-level storage.

        Example:
            >>> WeekPatternManager.clear()
        """
        WeekPattern.week_patterns = []

class MonthPattern:
    """Represents a 4-week structured month schedule built from saved week pattern references.

    Attributes:
        monthPatterns (dict[str, list[str]]): Class-level registry mapping month pattern
            names to ordered 4-element lists of week pattern names (or 'skip').

    Example:
        >>> mp = MonthPattern('month1')
        >>> mp.set_month_pattern(['week1', 'week2', 'skip', 'week4'])
    """
    monthPatterns = dict()
    def __init__(self,name):
        """Initializes a new MonthPattern instance.

        Args:
            name (str): Unique identifier for this month pattern.

        Example:
            >>> mp = MonthPattern('january_schedule')
        """
        self.__name = name
        self.__month_pattern = []
        self.__week_patterns = WeekPattern.week_patterns

    def set_month_pattern(self,month_pattern):
        """Sets the sequence of week pattern references for this month.

        Args:
            month_pattern (list[str]): Ordered list of week pattern names or 'skip'.

        Example:
            >>> mp.set_month_pattern(['week1', 'skip', 'week1', 'skip'])
        """
        self.__month_pattern = month_pattern
    
    def set_week_patterns(self,week_patterns):
        """Updates the internal reference to registered week patterns.

        Args:
            week_patterns (dict[str, list[str]]): Dictionary of available week patterns.

        Example:
            >>> mp.set_week_patterns({'week1': ['mon', 'wed']})
        """
        self.__week_patterns = week_patterns

    def get_week_patterns(self):
        """Retrieves registered week pattern references associated with this month pattern.

        Returns:
            dict[str, list[str]]: Map of week pattern names to active weekday lists.

        Example:
            >>> mp.get_week_patterns()
            {'week1': ['mon', 'wed']}
        """
        return self.__week_patterns

    def get_month_pattern(self):
        """Retrieves the sequence of week pattern references defining this month.

        Returns:
            list[str]: Ordered sequence of week pattern names or 'skip' tokens.

        Example:
            >>> mp.get_month_pattern()
            ['week1', 'skip', 'week1', 'skip']
        """
        return self.__month_pattern
    
    def get_name(self):
        """Retrieves the name of this month pattern.

        Returns:
            str: The unique month pattern identifier.

        Example:
            >>> mp.get_name()
            'january_schedule'
        """
        return self.__name
    
    def set_name(self,name):
        """Updates the name of this month pattern.

        Args:
            name (str): The new unique month pattern name.

        Example:
            >>> mp.set_name('february_schedule')
        """
        self.__name = name

class MonthPatternManager:
    """Manages creation, updates, lookup, and deletion of `MonthPattern` instances.

    Example:
        >>> manager = MonthPatternManager()
        >>> manager.save_month_pattern('m1', ['w1', 'w2', 'w3', 'w4'])
        (True, 'month pattern saved successfully')
    """
    def find_month_pattern(self,name):
        """Finds a saved month pattern by name.

        Args:
            name (str): The name of the month pattern to look up.

        Returns:
            list[str] | None: List of week pattern references if found, otherwise None.

        Example:
            >>> manager.find_month_pattern('m1')
            ['w1', 'w2', 'w3', 'w4']
        """
        return MonthPattern.monthPatterns.get(name,None)

    def delete_month_pattern(self,name):
        """Removes a saved month pattern from the registry.

        Args:
            name (str): The name of the month pattern to delete.

        Returns:
            list[str] | None: The removed week pattern list if found, otherwise None.

        Example:
            >>> manager.delete_month_pattern('m1')
            ['w1', 'w2', 'w3', 'w4']
        """
        return MonthPattern.monthPatterns.pop(name,None)

    def update_month_pattern(self,name,month_pattern):
        """Updates an existing month pattern configuration.

        Args:
            name (str): Name of the month pattern to update.
            month_pattern (list[str]): New 4-week list of pattern names.

        Example:
            >>> manager.update_month_pattern('m1', ['w1', 'skip', 'w1', 'skip'])
        """
        if name in MonthPattern.monthPatterns:
            MonthPattern.monthPatterns[name] = month_pattern

    def get_saved_months(self):
        """Retrieves all stored month patterns.

        Returns:
            dict[str, list[str]]: Dictionary mapping month pattern names to week lists.

        Example:
            >>> manager.get_saved_months()
            {'m1': ['w1', 'skip', 'w1', 'skip']}
        """
        return MonthPattern.monthPatterns

    def save_month_pattern(self,name,month_pattern):
        """Saves a new month pattern configuration if the name is unique.

        Args:
            name (str): Unique identifier for the month pattern.
            month_pattern (list[str]): Ordered list of 4 week pattern identifiers or 'skip'.

        Returns:
            tuple[bool, str]: A tuple containing success boolean and status message.

        Example:
            >>> manager.save_month_pattern('m2', ['w1', 'w1', 'w1', 'w1'])
            (True, 'month pattern saved successfully')
        """
        if name not in MonthPattern.monthPatterns:
            MonthPattern.monthPatterns[name] = month_pattern
            return True,'month pattern saved successfully'
        return False, f'Sorry new month pattern with name \'{name}\' already exists'

    @classmethod   
    def clear(cls):
        """Clears all saved month patterns from class-level storage.

        Example:
            >>> MonthPatternManager.clear()
        """
        MonthPattern.monthPatterns = []

class MonthsPattern:
    """Represents a multi-month schedule pattern combining multiple month pattern references.

    Example:
        >>> mp = MonthsPattern()
        >>> mp.set_months_pattern(['month1', 'skip', 'month2'])
        >>> mp.save_months_pattern()
        (True, 'success...')
    """
    def __init__(self):
        """Initializes an empty MonthsPattern structure."""
        self.__months_pattern = []

    def set_months_pattern(self,months_pattern):
        """Assigns a raw list of month pattern names or 'skip' tokens.

        Args:
            months_pattern (list[str]): List of month pattern names (e.g., ['month1', 'month2', 'skip']).

        Example:
            >>> mp.set_months_pattern(['m1', 'skip', 'm2'])
        """
        self.__months_pattern = months_pattern
    
    def get_months_pattern(self):
        """Retrieves the current multi-month schedule pattern structure.

        Returns:
            list[str | dict[str, list[str]]]: Raw month identifiers or fully expanded month mapping dictionaries.

        Example:
            >>> mp.get_months_pattern()
            ['m1', 'skip', 'm2']
        """
        return self.__months_pattern
    
    def save_months_pattern(self):
        """Expands raw month pattern names into full nested dictionary mappings.

        Replaces each month pattern name with its corresponding dictionary definition 
        from `MonthPattern.monthPatterns`, or maps `'skip'` to `{'skip': ''}`.

        Returns:
            tuple[bool, str]: A tuple containing success boolean and status outcome.

        Example:
            >>> MonthPattern.monthPatterns = {'m1': ['w1', 'w2', 'w3', 'w4']}
            >>> mp.set_months_pattern(['m1', 'skip'])
            >>> mp.save_months_pattern()
            (True, 'success...')
            >>> mp.get_months_pattern()
            [{'m1': ['w1', 'w2', 'w3', 'w4']}, {'skip': ''}]
        """
        self.__months_pattern  = [
            {month_pattern:MonthPattern.monthPatterns[month_pattern]}
            if month_pattern!='skip'
            else {'skip':''}
            for month_pattern in self.__months_pattern 
        ]
        return True,'success...'