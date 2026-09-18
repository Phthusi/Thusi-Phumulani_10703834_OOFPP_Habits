import unittest
from src.components.time_project.time_manager import HabitDateTimeManager
from datetime import timedelta

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
        pass

    def test_is_clashing(self):
        pass

    def test_determine_habit_status(self):
        pass
    
if __name__=='__main__':
    unittest.main()