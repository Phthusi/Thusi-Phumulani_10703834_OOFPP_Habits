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

class TestDateTimeManager(unittest.TestCase):
    def setUp(self):
        self.__habit_datetime_manager = HabitDateTimeManager()
        self.__habit_datetime_validator = HabitDateTimeManager()

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
        self.assertEqual(self.__habit_datetime_manager.determine_habit_status('2026-09-06 14:00:00','00:30:00'),'MISSED')
        self.assertEqual(self.__habit_datetime_manager.determine_habit_status('2029-09-06 14:00:00','00:30:00'),'UPCOMING')
        today = datetime.now()
        date = today.date()
        todays_day = date.day
        todays_year = date.year
        todays_month = date.month
        time = today.time()
        today_hour = time.hour
        today_minutes = time.minute
        today_second = time.second
        self.assertEqual(self.__habit_datetime_manager.determine_habit_status(f'{todays_year}-{todays_month}-{todays_day} {today_hour}:{today_minutes}:{today_second}','00:30:00'),'ONGOING')

        today = today - timedelta(hours=4)
        todays_day = date.day
        todays_year = date.year
        todays_month = date.month
        time = today.time()
        today_hour = time.hour
        today_minutes = time.minute
        today_second = time.second
        self.assertEqual(self.__habit_datetime_manager.determine_habit_status(f'{todays_year}-{todays_month}-{todays_day} {today_hour}:{today_minutes}:{today_second}','00:30:00'),'TO_BE_CONFIRMED')

    def test_convert_duration(self): 
        time_delta = self.__habit_datetime_manager.convert_duration('14:30:45')
        self.assertEqual(time_delta,timedelta(hours=14,minutes=30,seconds=45))

        with self.assertRaises(ValueError) as context:
            self.__habit_datetime_manager.convert_duration('25:56:11')

        self.assertEqual(str(context.exception),'invalid format:Hours(0-23):Minutes(0-59):Seconds(0-59)')

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