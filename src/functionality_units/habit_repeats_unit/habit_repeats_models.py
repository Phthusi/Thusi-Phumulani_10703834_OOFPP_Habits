from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent


'''
on the flow

1st when someone says daily = week pattern i.e mon,tue,wed,thu,fri,sat,sun
2nd still has to give the number of months to repeat the habit for

1st when someone says weekly = do it once a week
2nd give us a day of the week to repeat the habit on

when someone says monthly = do it once a month
2nd give us a weekdday of the month to repeat the habit on
'''
class WeekPattern:
    '''
    must not be empty
    e.g mon fri sat
    mon
    '''
    week_patterns = dict()
    def __init__(self,name):
        self.name = name
        self.__week_pattern = []

    def set_week_pattern(self,week_pattern):
        self.__week_pattern = week_pattern

    def get_week_pattern(self):
        return self.__week_pattern
    
    def get_name(self):
        return self.__name
    
    def set_name(self,name):
        self.__name = name
        
    def __repr__(self):
        return f"week_name: {self.get_name()}{'\n '.join(list(map(lambda day: day.upper(),self.get_week_pattern())))}"

class WeekPatternManager:
    def find_week_pattern(self,name):
        return WeekPattern.week_patterns.get(name,None)

    def delete_week_pattern(self,name):
        WeekPattern.week_patterns.pop(name,None)

    def update_week_pattern(self,name,week_pattern):
        if name in WeekPattern.week_patterns:
            WeekPattern.week_patterns[name] = week_pattern

    def save_week_pattern(self,name,week_pattern):
        if name not in WeekPattern.week_patterns:
            WeekPattern.week_patterns[name] = week_pattern
            return True,'week pattern saved successfully'
        return False, f'Sorry new week pattern with name \'{name}\' already exists'

class MonthPattern:
    '''
    must not be empty

    week1
    mon fri sat
    
    week2
    mon tue wed thu fri sat

    month
    week1 week2 week3 week4
    week1 skip week2 week3 week4
    '''
    monthPatterns = dict()
    def __init__(self,name):
        self.__name = name
        self.__month_pattern = []
        self.__week_patterns = []

    def set_month_pattern(self,month_pattern):
        self.__month_pattern = month_pattern
    
    def set_week_patterns(self,week_patterns):
        self.__week_patterns = week_patterns

    def get_week_patterns(self):
        return self.__week_patterns

    def get_month_pattern(self):
        return self.__month_pattern
    
    def get_name(self):
        return self.__name
    
    def set_name(self,name):
        self.__name = name

class MonthPatternManager:
    def find_month_pattern(self,name):
        return MonthPattern.monthPatterns.get(name,None)

    def delete_month_pattern(self,name):
        return MonthPattern.monthPatterns.pop(name,None)

    def update_month_pattern(self,name,month_pattern):
        if name in MonthPattern.monthPatterns:
            MonthPattern.monthPatterns[name] = month_pattern

    def save_month_pattern(self,name,month_pattern):
        if name not in MonthPattern.monthPatterns:
            MonthPattern.monthPatterns[name] = month_pattern

class MonthPatterns:
    '''

    '''
    monthPatterns = dict()
    def __init__(self,name):
        self.__name = name
        self.__month_pattern = []
        self.__week_patterns = []

    def set_month_pattern(self,month_pattern):
        self.__month_pattern = month_pattern
    
    def set_week_patterns(self,week_patterns):
        self.__week_patterns = week_patterns

    def get_week_patterns(self):
        return self.__week_patterns

    def get_month_pattern(self):
        return self.__month_pattern
    
    def get_name(self):
        return self.__name
    
    def set_name(self,name):
        self.__name = name