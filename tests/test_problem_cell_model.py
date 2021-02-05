
import unittest
from models.problem_cell_model import ProblemCellModelBuilder
from APImodels.problem import Problem
from APImodels.grade import Grade
from APImodels.RIC import RIC
from APImodels.colour import Colour
from datetime import date

class TestProblemCellModel(unittest.TestCase):

    def setUp(self):
        self.problem = Problem(
            2, 
            RIC(1,2,3), 
            Grade('purple', 'mid'), 
            'purple',  
            'cave l', 
            ['pop', 'layback', 'power'], 
            'Thara', 
            date.today(),
            'on')
        self.builder = ProblemCellModelBuilder()

    def test_build_from_problem(self):
        model = self.builder.build_from_problem(self.problem)

        self.assertEqual(model.row, 6)
        self.assertEqual(model.col, 3)
        self.assertEqual(model.bg_colour.to_tuple(),    Colour(131,113,187).to_tuple())
        self.assertEqual(model.text_colour.to_tuple(),  Colour(  0,  0,  0).to_tuple())
        self.assertEqual(model.hover_colour.to_tuple(), Colour(171,157,208).to_tuple())
        self.assertEqual(model.text, 'pop')
        self.assertEqual(model.RIC, '1 2 3')
        self.assertEqual(model.id, 2)
        
    
    def test_build_from_row_col(self):
        model = self.builder.build_from_row_col(1,2)

        self.assertEqual(model.row, 1)
        self.assertEqual(model.col, 2)
        self.assertEqual(model.bg_colour.to_tuple(),    Colour( 30, 30, 30).to_tuple())
        self.assertEqual(model.text_colour.to_tuple(),  Colour(240,240,240).to_tuple())
        self.assertEqual(model.hover_colour.to_tuple(), Colour( 60, 60, 60).to_tuple())
        self.assertEqual(model.text, '')
        self.assertEqual(model.RIC, '')
        self.assertEqual(model.id, 0)