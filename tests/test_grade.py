# tests for Grade

import unittest
from APImodels.grade import Grade

class TestGrade(unittest.TestCase):

    def test_from_str(self):
        result  = Grade.from_str(' purple hard ')
        grade_2 = Grade.from_str(' Purple hard ')

        self.assertEqual(result.range, 'purple')
        self.assertEqual(result.difficulty, 'hard')
        self.assertEqual(grade_2.range, 'purple')