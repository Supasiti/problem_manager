# test sector

from sector import Sector
from problem import Problem
import unittest

class TestSector(unittest.TestCase):

    def setUp(self):
        self.id1 = 1
        self.id2 = 2
        self.id3 = 3
        self.ids = [self.id1, self.id2, self.id3, 'a']
        self.sector = Sector('Front')

    def test_add_nothing(self):
        with self.assertRaises(ValueError):
            self.sector.add_problems()  

    def test_add_problem(self):
        self.sector.add_problems(self.id1)  

        self.assertEqual(self.sector.contains_problem(1), True)

    def test_add_problems(self):
        self.sector.add_problems(self.ids)

        self.assertEqual(self.sector.contains_problem(3), True)
        self.assertEqual('a' in self.sector._problem_ids, False)

if __name__ == '__main__':
    unittest.main()
