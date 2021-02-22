import unittest
import datetime 

from APImodels.RIC import RIC
from APImodels.grade import Grade
from APImodels.problem import Problem
from services.problems_editor import ProblemsEditor, EditingProblemsEditor
from services.problem_repository import ProblemRepository

class TestProblemEditor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = MockRepository()
        cls.editor     = ProblemsEditor(EditingProblemsEditor())

    def setUp(self):
        self.editor.load_problems(self.repository)

    def test_load_problems(self):
        problems = self.editor.problems
        next_id  = self.editor.next_id

        self.assertTupleEqual(problems, self.repository.problems)
        self.assertEqual(next_id, 4)

    def test_next_id(self):
        _id = self.editor.next_available_problem_id()

        self.assertEqual(_id, 4)

    def test_get_problem_by_id(self):
        problem = self.editor.get_problem_by_id(2)

        self.assertEqual(problem, self.repository.problems[1])
    
    def test_add_same_problem(self):
        problem1 = Problem(id=1, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem1)
        problems = self.editor.problems
        problem  = self.editor.get_problem_by_id(1)

        self.assertEqual(len(problems), 3)
        self.assertEqual(problem, problem1)

    def test_add_new_problem(self):
        problem4 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem4)
        problems = self.editor.problems
        problem  = self.editor.get_problem_by_id(4)

        self.assertEqual(len(problems), 4)
        self.assertEqual(problem, problem4)

    def test_add_incorrect_problem(self):
        problem5 = Problem(id=5, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        with self.assertRaises(ValueError):
            self.editor.add_new_problem(problem5)
       
    def test_delete_problem(self):
        problem4 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem4)   
        self.editor.delete_problem(2)
        self.editor.delete_problem(4)
        result2 = self.editor.get_problem_by_id(2)
        result4 = self.editor.get_problem_by_id(4)
        
        self.assertEqual(type(result2), Problem)
        self.assertEqual(result4, None)

    def test_strip_problem(self):
        problem4 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem4)
        self.editor.strip_problem(2, datetime.date.today())
        with self.assertRaises(IndexError):
            self.editor.strip_problem(4, datetime.date.today())
        problems = self.editor.problems
        problem  = self.editor.get_problem_by_id(2)

        self.assertEqual(len(problems),3)
        self.assertEqual(problem, None)


class MockRepository(ProblemRepository):

    def __init__(self):

        self.problems = (
            Problem(id=1, RIC=RIC(4, 4, 3), grade=Grade('red', 'mid'), colour='red', sector='arch l', styles=('toe hook', 'pop'), set_by='Thara', set_date=datetime.date(2021, 1, 2), strip_date=None), 
            Problem(id=2, RIC=RIC(5, 2, 3), grade=Grade('black', 'mid'), colour='orange', sector='arch l', styles=('run', 'press'), set_by='Aaron', set_date=datetime.date(2021, 2, 2), strip_date=None), 
            Problem(id=3, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        )
        self._next_id = 4

    def get_all_problems(self):
        return self.problems
    
    def get_problem_by_id(self):
        pass

    @property
    def next_id(self):
        return self._next_id


