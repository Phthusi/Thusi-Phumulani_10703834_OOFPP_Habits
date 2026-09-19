import unittest
from ..habit_validator import HabitValidator
from ..habit import Habit

class TestHabitValidator(unittest.TestCase):
    def setUp(self):
        self.__habit = Habit("default","default","default")
        self.__habit_validator = HabitValidator(self.__habit)

    def test_valid_name_empty(self):
        is_name_valid,message = self.__habit_validator.valid_name()
        self.assertFalse(is_name_valid)
        self.assertEqual(message,"Name cannot be empty.")

    def test_valid_name_with_nonstring_input(self):
        self.__habit.set_name(2)
        is_name_valid,message = self.__habit_validator.valid_name()
        self.assertFalse(is_name_valid)
        self.assertEqual(message,"Name must be a string.")

    def test_valid_name_with_less_than_3_chars(self):
        self.__habit.set_name('do')
        is_name_valid,message = self.__habit_validator.valid_name()
        self.assertFalse(is_name_valid)
        self.assertEqual(message,"Name must be at least 3 characters long.")

    def test_valid_name_with_valid_name(self):
        self.__habit.set_name('awesome')
        is_name_valid,message = self.__habit_validator.valid_name()
        self.assertTrue(is_name_valid)
        self.assertEqual(message,"name is valid.")

    def test_valid_session_duration_empty(self):
        is_duration_valid,message = self.__habit_validator.valid_session_duration()
        self.assertFalse(is_duration_valid)
        self.assertEqual(message,"Session duration must be a string.")

    def test_valid_session_duration_with_non_string_input(self):
        self.__habit.set_session_duration(56)
        is_duration_valid,message = self.__habit_validator.valid_session_duration()
        self.assertFalse(is_duration_valid)
        self.assertEqual(message,"Session duration must be a string.")

    def test_valid_session_duration_with_bad_format(self):
        self.__habit.set_session_duration('this is bad')
        is_duration_valid,message = self.__habit_validator.valid_session_duration()
        self.assertFalse(is_duration_valid)
        self.assertEqual(message,"Session duration must use HH:MM:SS with valid values.")

    def test_valid_session_duration_with_valid_input(self):
        self.__habit.set_session_duration('14:00:01')
        is_duration_valid,message = self.__habit_validator.valid_session_duration()
        self.assertTrue(is_duration_valid)
        self.assertEqual(message,"session duration is valid.")

    def test_valid_status_empty(self):
        is_status_valid,message = self.__habit_validator.valid_status()
        self.assertTrue(is_status_valid)
        self.assertEqual(message,"status is valid.")

    def test_valid_status_with_invalid_input(self):
        self.__habit.set_status("invalid")
        is_status_valid,message = self.__habit_validator.valid_status()
        self.assertFalse(is_status_valid)
        self.assertEqual(message,"Status must be one of: UPCOMING, IN_PROGRESS, COMPLETED, MISSED.")

    def test_valid_status_with_valid_inputs(self):
        statuses = ["UPCOMING","IN_PROGRESS","TO_BE_CONFIRMED","COMPLETED","MISSED"]
        for status in statuses:
            with self.subTest(status=status):
                self.__habit.set_status(status)
                self.assertTrue(self.__habit_validator.valid_status())

    def test_valid_status_with_invalid_input(self):
        self.__habit.set_status("COMPELTED")
        is_status_valid,message = self.__habit_validator.valid_for_updating()
        self.assertFalse(is_status_valid)
        self.assertEqual(message,"Habit cannot be updated because it has passed or it was completed")

    def test_valid_status_with_invalid_input(self):
        is_status_valid,message = self.__habit_validator.valid_for_updating()
        self.assertTrue(is_status_valid)
        self.assertEqual(message,"Habit can be updated.")

    def test_valid_start_datetime_empty(self):
        is_start_datetime_valid,message = self.__habit_validator.valid_start_date()
        self.assertFalse(is_start_datetime_valid)
        self.assertEqual(message,"Start datetime must be a datetime or a datetime string.")

    def test_valid_start_datetime_with_valid_input(self):
        self.__habit.set_start_date('2001-02-15 15:12:00')
        is_start_datetime_valid,message = self.__habit_validator.valid_start_date()
        self.assertTrue(is_start_datetime_valid)
        self.assertEqual(message,"start datetime is valid.")

    def test_valid_id_empty(self):
        is_id_valid,message = self.__habit_validator.valid_id()
        self.assertTrue(is_id_valid)
        self.assertEqual(message,"id is valid.")

    def test_valid_id_with_valid_input(self):
        self.__habit = Habit("default","default","default",id=1)
        self.__habit_validator.habit = self.__habit
        is_id_valid,message = self.__habit_validator.valid_id()
        self.assertTrue(is_id_valid)
        self.assertEqual(message,"id is valid.")

    def test_valid_id_with_invalid_input(self):
        self.__habit = Habit("default","default","default",id="1")
        self.__habit_validator.habit = self.__habit
        is_id_valid,message = self.__habit_validator.valid_id()
        self.assertFalse(is_id_valid)
        self.assertEqual(message,"ID must be an integer or None.")

    def test_validate(self):
        habits = [
            Habit("running","00:30:00","2001-02-15 15:12:00",id=1),
            Habit("default","default","default"),
            Habit(1,"default","default"),
            Habit("de","default","default"),
            Habit("default","default","default",id="this"),
            Habit("running","default","2001-02-15 15:12:00"),
            Habit("running",2,"default"),
            Habit("running","invalid duration","default"),
            Habit("running","00:30:00","2001-02-15 15:12:00",status='default'),
            Habit("running","00:30:00","2001-02-15 15:12:00",status='SOME STATUS'),
            Habit("running","default","default")
        ]

        # method_pairs = [
        #     (
        #     lambda :self.assertTrue(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Habit is valid.',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Name cannot be empty',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Name must be a string.',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Name must be at least 3 characters long.',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('ID must be an integer or None.',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Duration cannot be empty',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('session datetime must be a string',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Duration must use HH:MM:SS.',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Status cannot be empty',self.__habit_validator.validate()[1]),
        #     ),
        #     (
        #     lambda :self.assertFalse(self.__habit_validator.validate()[0]),
        #     lambda:self.assertEqual('Status must be one of: UPCOMING, IN_PROGRESS, COMPLETED, MISSED.',self.__habit_validator.validate()[1]),
        #     ),
        # ]

        # for method_pair, habit in zip(method_pairs,habits):
        #     self.__habit_validator.set_habit(habit)
        #     with self.subTest(habit_name=f'{habit.get_name()}'):
        #         method1,method2 = method_pair
        #         method1()
        #         method2()

if __name__=='__name__':
    unittest.main()
