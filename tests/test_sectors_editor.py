import unittest

from services.sector_editor import SectorEditor

class TestSectorEditor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = MockRepository()
        cls.editor     = SectorEditor()

    def setUp(self):
        self.editor.load_sectors(self.repository)

    def test_get(self):
        col = self.editor.get_col('mid')
        sector = self.editor.get_sector(9)
        sectors = self.editor.get_all_sectors()
        from_mock = tuple(self.repository.sectors.keys())
        length = self.editor.length()

        self.assertEqual(col, 2)
        self.assertEqual(sector, 'slab r')
        self.assertTupleEqual(sectors, from_mock)
        self.assertEqual(length, 13)

    def test_add_sector(self):
        with self.assertRaises(ValueError):
            self.editor.add_sector('mid', 1)
        with self.assertRaises(ValueError):
            self.editor.add_sector('cave', -1)
        
        self.editor.add_sector('cave', 14)
        col = self.editor.get_col('cave')
        self.assertEqual(col, 13)

        self.editor.add_sector('star', 8)
        col  = self.editor.get_col('star')
        col2 = self.editor.get_col('cave')
        self.assertEqual(col, 8)
        self.assertEqual(col2, 14)

    def test_remove_sector(self):
        with self.assertRaises(ValueError):
            self.editor.remove_sector('cave')
        
        self.editor.remove_sector('35c')
        with self.assertRaises(ValueError):
            self.editor.get_col('35c')

        col = self.editor.get_col('arch r')
        self.assertEqual(col, 7)

    def test_move_sector_up(self):
        with self.assertRaises(ValueError):
            self.editor.move_sector('cave', 1)
        with self.assertRaises(ValueError):
            self.editor.move_sector('mid', 14)

        self.editor.move_sector('mid', 4)
        col2 = self.editor.get_col('tower')
        col3 = self.editor.get_col('hangover l')
        col4 = self.editor.get_col('mid')
        self.assertEqual(col2, 2)
        self.assertEqual(col3, 3)
        self.assertEqual(col4, 4)

    def test_move_sector_down(self):
        self.editor.move_sector('hangover l', 2)
        col2 = self.editor.get_col('hangover l')
        col3 = self.editor.get_col('mid')
        col4 = self.editor.get_col('tower')
        self.assertEqual(col2, 2)
        self.assertEqual(col3, 3)
        self.assertEqual(col4, 4)
    
    def test_change_to(self):
        with self.assertRaises(ValueError):
            self.editor.change_name('cave', 'new')
        with self.assertRaises(ValueError):
            self.editor.change_name('mid', 'tower')

        self.editor.change_name('mid', 'cave')

        with self.assertRaises(ValueError):
            self.editor.get_col('mid')
        col = self.editor.get_col('cave')
        self.assertEqual(col, 2)

class MockRepository():

    def __init__(self):

        self.sectors = {
                "front l" : 0,
                "front r" : 1,
                "mid"     : 2,
                "tower"      : 3,
                "hangover l" : 4,
                "hangover r" : 5,
                "back slab" : 6,
                "35c"       : 7,
                "arch r"  : 8,
                "slab r"  : 9,
                "arch l"  : 10,
                "slab l"  : 11,
                "slab"    : 12
            }

    def get_all_problems(self):
        pass
    
    def get_problem_by_id(self):
        pass

    def get_all_sectors(self):
        return self.sectors.copy()

    @property
    def next_id(self):
        pass