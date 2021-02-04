# tests for RIC
import unittest
from models.RIC import RIC

class TestRIC(unittest.TestCase):

    def test_constructer(self):
        self.ric = RIC(1,2,3)

        self.assertEqual(self.ric.R, 1)
        self.assertEqual(self.ric.I, 2)
        self.assertEqual(self.ric.C, 3)

    def test_construct_with_string(self):
        with self.assertRaises(TypeError):
            self.ric = RIC('1',2,5)

    def test_construct_with_out_of_range_value(self):
        with self.assertRaises(ValueError):
            self.ric = RIC(1,2,6)

    def test_try_set_value(self):
        self.ric = RIC(1,2,3)
        with self.assertRaises(AttributeError):
            self.ric.R = 2
