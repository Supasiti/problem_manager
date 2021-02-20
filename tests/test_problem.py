import unittest


from APImodels.problem import Problem
from APImodels.RIC import RIC
from APImodels.grade import Grade
import datetime

class TestProblem(unittest.TestCase):

    def setUp(self):
        self.problem = Problem(id=1, RIC=RIC(4, 4, 3), grade=Grade('red', 'mid'), colour='red', sector='arch l', styles=('toe hook', 'pop'), set_by='Thara', set_date=datetime.date(2021, 1, 2), status='on')


    def test_to_dict(self):
        problem_dict = self.problem.to_dict()

        self.assertEqual(problem_dict['id'], 1)
        self.assertEqual(problem_dict['RIC'],   RIC(4,4,3).to_dict())
        self.assertEqual(problem_dict['grade'],    Grade('red', 'mid')._asdict())
        self.assertEqual(problem_dict['colour'],   'red')
        self.assertEqual(problem_dict['sector'],   'arch l')
        self.assertEqual(problem_dict['styles'],   ('toe hook', 'pop'))
        self.assertEqual(problem_dict['set_by'],   'Thara')
        self.assertEqual(problem_dict['set_date'], '2021-01-02')
        self.assertEqual(problem_dict['status'],   'on')

    def test_eq(self):
        other = Problem(id=1, RIC=RIC(4, 4, 3), grade=Grade('red', 'mid'), colour='red', sector='arch l', styles=('toe hook', 'pop'), set_by='Thara', set_date=datetime.date(2021, 1, 2), status='on')
        self.assertEqual(self.problem, other) 

