# import unittest
# from ..terminal_utils import retry_until_success

# def add_numbers(*args,**kwargs):
#     if 'number' in kwargs.keys() and 'limit' in kwargs.keys():
#         if kwargs['number'] < kwargs['limit']:
#            return False,'blah blah blah'
#         return True,'blew blew blew'

# results = []
# number=-1

# @retry_until_success
# def call_add_numbers(self,limit=3):
#     global number
#     number+=1
#     result = add_numbers(number=number,limit=limit)
#     results.append(result)
#     return result

# class TestTerminalUtils(unittest.TestCase):
#     def setUp(self):
#         pass

#     def test_retry_until_success(self):
#         call_add_numbers(self,limit=3)
#         self.assertEqual(len(results),4)
#         self.assertEqual([
#             (False,'blah blah blah'),
#             (False,'blah blah blah'),
#             (False,'blah blah blah'),
#             (True,'blew blew blew'),
#             ],results)
        
#     # def test_retry_until_success(self):
#     #     call_add_numbers(self,limit=1)
#     #     self.assertEqual(len(results),4)
#     #     self.assertEqual([
#     #         (False,'blah blah blah'),
#     #         (False,'blah blah blah'),
#     #         (False,'blah blah blah'),
#     #         (True,'blew blew blew'),
#     #         ],results)