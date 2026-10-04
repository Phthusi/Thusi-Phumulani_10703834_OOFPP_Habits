from .habit_repeats_models import WeekPattern,MonthPattern, MonthsPattern

class WeekPatternValidator:
    """Validates week pattern names, weekday selections, and overall week pattern structures.

    Args:
        week_pattern (WeekPattern): An instance of `WeekPattern` to validate.

    Example:
        >>> wp = WeekPattern('week1')
        >>> wp.set_week_pattern(['mon', 'wed', 'fri'])
        >>> validator = WeekPatternValidator(wp)
    """
    def __init__(self,week_pattern:WeekPattern):
        """Initializes the validator with a specific `WeekPattern` instance.

        Args:
            week_pattern (WeekPattern): Target `WeekPattern` instance.

        Example:
            >>> validator = WeekPatternValidator(WeekPattern('test_week'))
        """
        self.__week_pattern = week_pattern

    @classmethod
    def is_name_pattern_valid(cls,name,names):
        """Validates that a proposed week pattern name adheres to formatting rules and uniqueness.

        Rules verified:
        - Must be a string.
        - Must not contain spaces.
        - Must be at least 3 characters long.
        - Must contain only lowercase alphabets [a-z] and digits [0-9].
        - Must start with an alphabetic character [a-z].
        - Must not already exist in `names`.

        Args:
            name (str): Proposed name string to validate.
            names (list[str] | set[str]): Existing collection of used pattern names.

        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if the name meets all criteria, False otherwise.
                - str: Validation feedback message.

        Example:
            >>> WeekPatternValidator.is_name_pattern_valid('week1', ['workdays'])
            (True, 'name is valid')
            >>> WeekPatternValidator.is_name_pattern_valid('1week', [])
            (False, 'name must begin with an alphabet[a-z]')
        """
        min_length = 3
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        numbers = '0123456789'
        if not isinstance(name,str):
            return False,"name must be a string"

        if ' ' in name:
            return False,"name must not have a space"
 
        if len(name) < min_length:
            return False,"name must be at least 3 characters long" 

        if not all(list(map(lambda char:char in alphabet or char in numbers,name))):
            return False,"name must be only be comprised of numbers[0-9] and alphabets[a-z]"
        
        if name[0] in numbers:
            return False,"name must begin with an alphabet[a-z]"
        
        if name in names:
            return False,"name already exists"
        
        return True,"name is valid"
    
    @classmethod
    def week_pattern_exists(cls,name):
        """Checks if a week pattern name exists in the class-level `WeekPattern.week_patterns` dictionary.

        Args:
            name (str): The week pattern name to verify.

        Returns:
            bool: True if the name exists as a saved key, False otherwise.

        Example:
            >>> WeekPattern.week_patterns = {'week1': ['mon', 'tue']}
            >>> WeekPatternValidator.week_pattern_exists('week1')
            True
            >>> WeekPatternValidator.week_pattern_exists('week99')
            False
        """
        return name in WeekPattern.week_patterns.keys()

    @classmethod
    def is_week_pattern_valid(cls,pattern):
        """Validates a list of weekday string tokens against allowed calendar days.

        Args:
            pattern (list[str]): List of day tokens (e.g., ['mon', 'wed', 'fri']).

        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if all items are valid short weekday names and non-empty, False otherwise.
                - str: Outcome status message detailing any invalid day inputs.

        Example:
            >>> WeekPatternValidator.is_week_pattern_valid(['mon', 'tue', 'fri'])
            (True, 'week pattern is valid')
            >>> WeekPatternValidator.is_week_pattern_valid(['mon', 'funday'])
            (False, 'funday are not valid week days')
        """
        week_days = ["mon","tue","wed","thu","fri","sat","sun"]
        if not isinstance(pattern,list):
            return False,"week pattern must be a list"
        if pattern==[]:
            return False,"week pattern must not be empty"
        
        invalid_days = [day in week_days for day in pattern]
        if not all(invalid_days):
            return False,f"{', '.join([day for day in pattern if day not in week_days])} are not valid week days"
        return True,"week pattern is valid"
    
    def is_week_valid(self):
        """Validates both the name and weekday contents of the assigned `WeekPattern` instance.

        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if both name and pattern lists pass validation, False if either fails.
                - str: Validation feedback message.

        Example:
            >>> wp = WeekPattern('week1')
            >>> wp.set_week_pattern(['mon', 'tue'])
            >>> validator = WeekPatternValidator(wp)
            >>> validator.is_week_valid()
            (True, 'week pattern is valid')
        """
        name_valid, name_message = self.is_name_pattern_valid(self.__week_pattern.get_name())
        if not name_valid:
            return False,name_message
        
        pattern_valid, pattern_message = self.is_week_pattern_valid(self.__week_pattern.get_week_pattern())
        if not pattern_valid:
            return False,pattern_message
        
        return True,"week pattern is valid"

class MonthPatternValidator:
    """Validates 4-week month patterns and referenced week dependencies.

    Args:
        week_pattern (WeekPattern): Reference instance used to inspect saved week pattern dependencies.

    Example:
        >>> wp = WeekPattern('week1')
        >>> validator = MonthPatternValidator(wp)
    """
    def __init__(self,week_pattern:WeekPattern):
        """Initializes the MonthPatternValidator.

        Args:
            week_pattern (WeekPattern): WeekPattern reference object.

        Example:
            >>> validator = MonthPatternValidator(WeekPattern('ref'))
        """
        self.__week_pattern = week_pattern
  
    def is_month_pattern_valid(self,pattern):
        """Validates that a month pattern consists of exactly 4 recognized week pattern names or 'skip'.

        Args:
            pattern (list[str]): List of week pattern references (e.g., ['week1', 'week2', 'skip', 'week4']).

        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if pattern length is 4, not entirely skipped, and all tokens exist.
                - str: Detailed validation feedback message.

        Example:
            >>> WeekPattern.week_patterns = {'w1': ['mon'], 'w2': ['tue']}
            >>> validator.is_month_pattern_valid(['w1', 'w2', 'skip', 'w1'])
            (True, 'month pattern is valid')
            >>> validator.is_month_pattern_valid(['w1', 'w2'])
            (False, 'month must have 4 weeks')
        """
        if not isinstance(pattern,list):
            return False,"month pattern must be a list"
        if not pattern:
            return False,"month pattern must not be empty"
        if len(pattern)!=4:
            return False, "month must have 4 weeks"

        if all(map(lambda month: month=='skip',pattern)):
            return False, "month must have 4 skips"
        
        valid_weeks = list(self.__week_pattern.week_patterns.keys())
        valid_weeks.extend(['skip'])
        invalid_month = [month in valid_weeks for month in pattern]
        if not all(invalid_month):
            return False,f"{', '.join([month for month in pattern if month not in valid_weeks])} are not valid week days"
        return True,"month pattern is valid"

    def is_week_patterns_valid(self,week_patterns):
        """Validates a list of `WeekPattern` objects using `WeekPatternValidator`.

        Args:
            week_patterns (list[WeekPattern]): List of `WeekPattern` instances to validate.

        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if all week patterns are valid, False if any instance fails.
                - str: Validation feedback message from the failing instance or confirmation.

        Example:
            >>> wp1 = WeekPattern('w1')
            >>> wp1.set_week_pattern(['mon'])
            >>> validator.is_week_patterns_valid([wp1])
            (True, 'week patterns are valid')
        """
        week_validator = WeekPatternValidator()
        for week_pattern in week_patterns:
            success,message = week_validator.is_week_valid(week_pattern)
            if not success:
                return False,message
        return True,"week patterns are valid"

    @classmethod
    def month_pattern_exists(cls,name):
        """Checks if a month pattern name exists in `MonthPattern.monthPatterns`.

        Args:
            name (str): The name of the month pattern to look up.

        Returns:
            bool: True if the month pattern exists, False otherwise.

        Example:
            >>> MonthPattern.monthPatterns = {'m1': ['w1', 'w1', 'w1', 'w1']}
            >>> MonthPatternValidator.month_pattern_exists('m1')
            True
        """
        return name in MonthPattern.monthPatterns.keys()
    
class MonthsPatternValidator:
    """Validates top-level multi-month patterns against registered month patterns.

    Args:
        pattern (MonthPattern): Reference `MonthPattern` instance used for checking saved month keys.

    Example:
        >>> mp = MonthPattern('m1')
        >>> validator = MonthsPatternValidator(mp)
    """
    def __init__(self,pattern:MonthPattern):
        """Initializes the MonthsPatternValidator.

        Args:
            pattern (MonthPattern): Target `MonthPattern` reference object.

        Example:
            >>> validator = MonthsPatternValidator(MonthPattern('ref'))
        """
        self.__month_pattern = pattern

    def is_months_pattern_valid(self,pattern):
        """Validates that a multi-month list contains recognized month pattern names or 'skip'.

        Args:
            pattern (list[str]): List of month pattern names (e.g., ['month1', 'skip', 'month2']).

        Returns:
            tuple[bool, str]: A tuple containing:
                - bool: True if non-empty, not entirely made of 'skip', and all names are valid.
                - str: Outcome status message.

        Example:
            >>> MonthPattern.monthPatterns = {'m1': ['w1', 'w2', 'w3', 'w4']}
            >>> validator.is_months_pattern_valid(['m1', 'skip'])
            (True, 'months pattern is valid')
            >>> validator.is_months_pattern_valid(['skip', 'skip'])
            (False, 'months patterns must not be entirely be made up of skip patterns')
        """
        if not isinstance(pattern,list):
            return False,"months pattern must be a list"
        if not pattern:
            return False,"months pattern must not be empty"

        if all(map(lambda month: month=='skip',pattern)):
            return False, "months patterns must not be entirely be made up of skip patterns"
        
        valid_months = list(self.__month_pattern.monthPatterns.keys())
        valid_months.extend(['skip'])
        invalid_month = [month in valid_months for month in pattern]
        if not all(invalid_month):
            return False,f"{', '.join([month for month in pattern if month not in valid_months])} are not valid months"
        return True,"months pattern is valid"