# tests for Grade

import unittest
from grade import Grade

class TestRIC(unittest.TestCase):

    def test_not_one_of_accepted_grades(self):
        with self.assertRaises(ValueError):
            self.grade = Grade('hard', 'hard')

    def test_not_one_of_accepted_difficulties(self):
        with self.assertRaises(ValueError):
            self.grade = Grade('white', 'soft')
            
    def test_construct_with_uppercase(self):
        self.grade1 = Grade('Yellow', 'hard')
        self.grade2 = Grade('yellow', 'Hard')

        self.assertEqual(self.grade1.range, self.grade2.range)
        self.assertEqual(self.grade1.difficulty, self.grade2.difficulty)

if __name__ == '__main__':
    unittest.main()
    