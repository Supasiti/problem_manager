import unittest
import datetime

from services.old_problem_viewer import OldProblemViewer
from APImodels.problem import Problem
from APImodels.RIC import RIC
from APImodels.grade import Grade

class TestOldProblemViewer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_data = MockFileIO()
        cls.viewer = OldProblemViewer()
        cls.viewer.set_dir_IO(cls.mock_data)

    def setUp(self):
        self.viewer.set_dir_IO(self.mock_data)

    def test_get_risks(self):
        risks = self.viewer.get_risks()
        grades = self.viewer.get_grades()
        colours = list(self.viewer.get_holds())
        colours.sort()
        colours = tuple(colours)

        styles = list(self.viewer.get_styles())
        styles.sort()
        styles = tuple(styles)
        self.assertTupleEqual(risks, (1,))
        self.assertTupleEqual(grades, (Grade('purple','mid'),))
        self.assertTupleEqual(colours, ('purple','red'))
        self.assertTupleEqual(styles, ('dyno','glide','pop'))

    def test_set_filter_holds(self):
        self.viewer.set_filter_holds(['purple'])
        self.viewer.filter_problems()
        problems = self.viewer.problems
        ids = [p.id for p in problems]
        ids.sort()

        self.assertListEqual(ids, [10,12])

    def test_set_filter_styles(self):
        self.viewer.set_filter_styles(['dyno','glide'])
        self.viewer.filter_problems()
        problems = self.viewer.problems
        ids = [p.id for p in problems]
        ids.sort()

        self.assertListEqual(ids, [9,10,11])

class MockFileIO():

    data = tuple([
        Problem(id=12, RIC=RIC(1, 1, 1), grade=Grade('purple', 'mid'), colour='purple', sector='mid', styles=('pop',), set_by='d', set_date=datetime.date(2021, 2, 25), strip_date=datetime.date(2021, 2, 26)), 
        Problem(id=11, RIC=RIC(1, 1, 1), grade=Grade('purple', 'mid'), colour='red', sector='mid', styles=('dyno','pop'), set_by='d', set_date=datetime.date(2021, 2, 25), strip_date=datetime.date(2021, 2, 26)), 
        Problem(id=10, RIC=RIC(1, 1, 1), grade=Grade('purple', 'mid'), colour='purple', sector='mid', styles=('glide',), set_by='d', set_date=datetime.date(2021, 2, 25), strip_date=datetime.date(2021, 2, 26)), 
        Problem(id=9, RIC=RIC(1, 1, 1), grade=Grade('purple', 'mid'), colour='red', sector='front', styles=('dyno',), set_by='d', set_date=datetime.date(2021, 2, 25), strip_date=datetime.date(2021, 2, 26))
    ])

    def get_all_problems(self):
        return self.data
    
    def filter_problems_by(self, predicate) -> tuple[Problem,...]:
        return tuple([p for p in self.data if predicate(p)])