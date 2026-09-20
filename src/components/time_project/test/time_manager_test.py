import unittest
from src.components.time_project.time_manager import HabitDateTimeManager
from datetime import timedelta,datetime

class TestDateTimeValidator(unittest.TestCase):
    def setUp(self):
        self.__habit_datetime_validator = HabitDateTimeManager()

    def test_calculate_time_difference_simple_case(self):
        results = self.__habit_datetime_validator.calculate_time_difference('2001-10-01 13:00:00','2002-10-01 13:00:00')
        self.assertEqual(results,timedelta(days=365))

    def test_calculate_time_difference_moderate_case(self):
        results = self.__habit_datetime_validator.calculate_time_difference('2001-10-01 13:10:00','2002-10-01 13:00:00')
        self.assertEqual(results,timedelta(days=364,hours=23,minutes=50))

    def test_calculate_time_difference_complex_case(self):
        results = self.__habit_datetime_validator.calculate_time_difference('2001-08-25 13:10:00','2012-10-01 13:14:15')
        years = 11
        days = 6
        minutes = 4
        seconds = 15
        total_days = 365 * years + 28 + days +6
        self.assertEqual(results,timedelta(total_days,minutes=minutes,seconds=seconds))

    def test_is_time_already_passed(self):
        self.assertFalse(self.__habit_datetime_validator.is_time_already_passed('2090-11-28 23:15:00'))
        self.assertTrue(self.__habit_datetime_validator.is_time_already_passed('1990-11-28 14:00:00'))

    def test_is_clashing(self):
        self.assertFalse(self.__habit_datetime_validator.is_clashing(datetime.strptime('2010-06-10 12:10:00','%Y-%m-%d %H:%M:%S'),timedelta(minutes=30),datetime.strptime('2010-06-10 11:30:00','%Y-%m-%d %H:%M:%S'),timedelta(minutes=30)))
        self.assertTrue(self.__habit_datetime_validator.is_clashing(datetime.strptime('2010-06-10 12:10:00','%Y-%m-%d %H:%M:%S'),timedelta(minutes=30),datetime.strptime('2010-06-10 11:30:00','%Y-%m-%d %H:%M:%S'),timedelta(minutes=50)))

    def test_determine_habit_status(self):
        pass
    
    def test_convert_duration(self): 
        pass

    def test_string_to_datetime(self):
        pass

    def test_is_date_valid(self):
        pass

    def test_get_weekday(self):
        pass

    def test_increase_by_day(self):
        pass

if __name__=='__main__':
    unittest.main()