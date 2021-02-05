
import unittest
from APImodels.sector import Sector

class TestSector(unittest.TestCase):

    def setUp(self):
        self.sector = Sector('front l', 2, (3,4), False)

    def test_set_attribute(self):
        with self.assertRaises(AttributeError):
            self.sector.name = 'front'

    def test_add_new_problem(self):
        result = self.sector.with_new_problem(6)
        self.assertEqual(result, Sector('front l', 3, (3,4,6), False))
        self.assertEqual(self.sector, Sector('front l', 2, (3,4), False))
    
    def test_add_duplicate_problem(self):
        result = self.sector.with_new_problem(4)
        self.assertEqual(result, Sector('front l', 2, (3,4), False))
        self.assertEqual(self.sector, Sector('front l', 2, (3,4), False))

    def test_remove_problem(self):
        result = self.sector.with_a_problem_removed(4)
        self.assertEqual(result, Sector('front l', 1, (3,), False))
        self.assertEqual(self.sector, Sector('front l', 2, (3,4), False))

    def test_remove_problem_2(self):
        result = self.sector.with_a_problem_removed(5)
        self.assertEqual(result, Sector('front l', 2, (3,4), False))

    def test_with_new_set(self):
        result = self.sector.with_new_set(True)
        self.assertEqual(result, Sector('front l', 2, (3,4), True))
        self.assertEqual(self.sector, Sector('front l', 2, (3,4), False))
    
    def test_with_problem_clear(self):
        result = self.sector.with_problems_cleared()
        self.assertEqual(result, Sector('front l', 0, tuple(), False))
        self.assertEqual(self.sector, Sector('front l', 2, (3,4), False))