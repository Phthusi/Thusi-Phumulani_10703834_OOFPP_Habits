import unittest

class TestStuff(unittest.TestCase):

    def test_add(self):
        result = 2 + 3
        self.assertEqual(result, 5)

if __name__ == "__main__":
    unittest.main()