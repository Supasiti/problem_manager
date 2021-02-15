
import unittest
from APImodels.sector import Sector

class TestSector(unittest.TestCase):

    def setUp(self):
        self.sector = Sector('front l', 2, (3,4), False)

    def test_set_attribute(self):
        with self.assertRaises(AttributeError):
            self.sector.name = 'front'
