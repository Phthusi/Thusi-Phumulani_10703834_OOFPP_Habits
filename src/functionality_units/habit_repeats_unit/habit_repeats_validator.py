from .habit_repeats_models import WeekPattern,MonthPattern

class WeekPatternValidator:
    def __init__(self,week_pattern:WeekPattern):
        self.__week_pattern = week_pattern

    @classmethod
    def is_name_pattern_valid(cls,name):
        min_length = 3
        if not isinstance(name,str):
            return False,"name must be a string"
        
        if len(name) < min_length:
            return False,"name must be at least 3 characters long" 

        return True,"name is valid"
    
    @classmethod
    def week_pattern_exists(cls,name):
        return name in WeekPattern.week_patterns.keys()

    @classmethod
    def is_week_pattern_valid(cls,pattern):
        week_days = ["mon","tue","wed","thu","fri","sat","sun"]
        if not isinstance(pattern,list):
            return False,"week pattern must be a list"
        if not pattern:
            return False,"week pattern must not be empty"
        
        invalid_days = [day for day in pattern if day not in week_days]
        if invalid_days:
            return False,f"{', '.join(invalid_days)} are not valid week days"
        return True,"week pattern is valid"
    
    def is_week_valid(self):
        name_valid, name_message = self.is_name_pattern_valid(self.__week_pattern.get_name())
        if not name_valid:
            return False,name_message
        
        pattern_valid, pattern_message = self.is_week_pattern_valid(self.__week_pattern.get_week_pattern())
        if not pattern_valid:
            return False,pattern_message
        
        return True,"week pattern is valid"

class MonthPatternValidator:
    @classmethod
    def is_month_pattern_valid(cls,pattern):
        if not isinstance(pattern,list):
            return False,"month pattern must be a list"
        if not pattern:
            return False,"month pattern must not be empty"
        invalid_month = [month not in MonthPattern.monthPatterns.keys() for month in pattern]
        if invalid_month:
            return False,f"{', '.join(invalid_month)} are not valid month patterns"
        return True,"month pattern is valid"

    @classmethod
    def is_week_patterns_valid(cls,week_patterns):
        week_validator = WeekPatternValidator()
        for week_pattern in week_patterns:
            success,message = week_validator.is_week_valid(week_pattern)
            if not success:
                return False,message
        return True,"week patterns are valid"

    @classmethod
    def month_pattern_exists(cls,name):
        return name in MonthPattern.monthPatterns.keys()
    
    @classmethod
    def is_name_pattern_valid(cls,name):
        min_length = 3
        if not isinstance(name,str):
            return False,"name must be a string"
        
        if len(name) < min_length:
            return False,"name must be at least 3 characters long" 

        return True,"name is valid"