import unittest
from ..db import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.__database = Database(':memory:')
        self.__habits = []
        if not self._testMethodName=='test_add_habit':
            self.__habits = [
                ('running','12-11-2026 15:30:00','00:05:00','UPCOMING','DAILY'),
                ('studying','18-11-2026 15:00:00','00:30:00','UPCOMING','MONTHLY'),
                ('soccer practice','12-11-2026 10:00:00','00:05:00','UPCOMING','DAILY'),
            ]
            for habit in self.__habits:
                self.__database.add_habit(*habit)

    def test_add_habit(self):
        success,id = self.__database.add_habit('run','12-11-2026 15:30:00','00:05:00','UPCOMING','DAILY')
        self.assertEqual(success,'success')
        self.assertEqual(id,1)

    def test_delete_habit(self):
        success,message = self.__database.delete_habit(3)
        self.assertEqual(success,'success')
        self.assertIsNone(message)

    def test_get_all_habits(self):
        success,results = self.__database.get_all_habits()
        results.sort(key=lambda entry:entry[0])
        self.assertEqual(3,len(results))
        self.assertEqual(success,'success')
        self.assertEqual(self.__habits,list(map(lambda habit:habit[1:],results)))

    def test_update_habit(self):
        expected_habit = self.__habits[2]
        self.__database.update_habit(habit_id=2,name='studying mathematics')
        success,results = self.__database.get_all_habits()
        results.sort(key=lambda entry:entry[0])
        self.assertEqual(results[2][1:],expected_habit)