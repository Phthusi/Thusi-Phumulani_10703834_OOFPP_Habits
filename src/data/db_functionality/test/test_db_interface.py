from ..db_interface import DB_Interface
from seed_fixtures import seed
import unittest

class Test_DB_Interface(unittest.TestCase):
    def setUp(self):
        self.__db_interface = DB_Interface(':memory:')
        seed(':memory:',self.__db_interface)
    
    def test_id_in_db_basic(self):
      for id in range(1,93):
            with self.subTest(id=id):
                self.assertTrue(self.__db_interface._DB_Interface__id_in_db(id))

    def test_get_all_habits(self):
        self.assertEqual(92,len(self.__db_interface.get_all_habits()))

    def test_update_habit(self):
        habit = ('Study Python programming','2026-08-28 07:00:00','00:30:00','MISSED','DAILY')
        self.__db_interface.update_habit(92,**{'name':'Study Python programming','duration':'00:30:00'})
        target_habit = list(filter(lambda habit:habit[0]==92,self.__db_interface.get_all_habits()))
        self.assertEqual(len(target_habit),1)
        self.assertEqual(target_habit[0][1:],habit)

    def test_add_habit(self):
        self.__habits = [
            ('running','12-11-2026 15:30:00','00:05:00','UPCOMING','DAILY'),
            ('studying','18-11-2026 15:00:00','00:30:00','UPCOMING','MONTHLY'),
            ('soccer practice','12-11-2026 10:00:00','00:05:00','UPCOMING','DAILY'),
        ]
        for habit in self.__habits:
            self.__db_interface.add_habit(*habit)
        self.assertEqual(95,len(self.__db_interface.get_all_habits()))
        self.assertTrue(self.__db_interface._DB_Interface__id_in_db(95))

    def test_delete_habit(self):
        self.__db_interface.delete_habit(1)
        self.assertEqual(91,len(self.__db_interface.get_all_habits()))
        self.assertFalse(self.__db_interface._DB_Interface__id_in_db(1))

    def test_get_cached_data(self):
        self.assertEqual(92,len(self.__db_interface.get_cached_data()))
        self.__db_interface.delete_habit(1)
        self.assertEqual(91,len(self.__db_interface.get_cached_data()))
