import unittest
from src.components.time_project.time_manager_validator import HabitDateTimeManagerValidator

class TestDateTimeValidator(unittest.TestCase):
    def setUp(self):
        self.__habit_datetime_validator = HabitDateTimeManagerValidator()

    def test_is_date_valid_with_valid_date(self):
        is_date_valid = self.__habit_datetime_validator.is_date_valid('2001-10-29')
        self.assertTrue(is_date_valid)

    def test_is_date_valid_with_invalid_date(self):
        is_date_valid = self.__habit_datetime_validator.is_date_valid('2001-13-29')
        self.assertFalse(is_date_valid)

    def test_is_datetime_valid_with_valid_datetime(self):
        is_datetime_valid = self.__habit_datetime_validator.is_datetime_valid('2001-10-25 00:15:00')
        self.assertTrue(is_datetime_valid)

    def test_is_datetime_valid_with_invalid_datetime(self):
        is_datetime_valid = self.__habit_datetime_validator.is_datetime_valid('00:15:00 2001-10-25')
        self.assertFalse(is_datetime_valid)

    def test_is_datetime_valid_without_seconds(self):
        is_datetime_valid = self.__habit_datetime_validator.is_datetime_valid('2001-10-25 00:15')
        self.assertFalse(is_datetime_valid)

    def test_is_passed__with_passed_time_with_passed_datetime(self):
        is_datetime_passed = self.__habit_datetime_validator.is_passed('2001-10-25 00:15:00')
        self.assertFalse(is_datetime_passed)

    def test_is_passed__with_passed_time_with_future_datetime(self):
        is_datetime_passed = self.__habit_datetime_validator.is_passed('2080-10-25 00:15:00')
        self.assertTrue(is_datetime_passed)

    def test_is_time_format_valid_valid_with_valid_time_format(self):
        is_valid_time_format = self.__habit_datetime_validator.is_time_format_valid('00:15:00')
        self.assertTrue(is_valid_time_format)

    def test_is_time_format_valid_valid_with_invalid_time_format(self):
        is_valid_time_format = self.__habit_datetime_validator.is_time_format_valid('00:15')
        self.assertFalse(is_valid_time_format)

    def test_validate_duration_with_invalid_duration(self):
        message, is_valid_time_format = self.__habit_datetime_validator.validate_duration('00:15')
        self.assertFalse(is_valid_time_format)

    def test_validate_duration_with_valid_duration(self):
        message, is_valid_time_format = self.__habit_datetime_validator.validate_duration('00:15:00')
        self.assertTrue(is_valid_time_format)

if __name__=='__main__':
    unittest.main()