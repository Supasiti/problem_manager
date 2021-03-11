import unittest
import datetime 

from APImodels.RIC import RIC
from APImodels.grade import Grade
from APImodels.problem import Problem
from services.problems_editor import ProblemsEditor, EditingProblemsEditor
from services.problems_editor_history import ProblemsEditorHistory
from services.problem_repository import ProblemRepository

class TestProblemEditorHistory(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.repository = MockRepository()
        cls.editor     = ProblemsEditor(EditingProblemsEditor())

    def setUp(self):
        self.editor.load_problems(self.repository)
        self.history = ProblemsEditorHistory(self.editor)
        self.history.backup()
        
    def test_backup_then_undo(self):
        problem4 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem4)
        self.assertEqual(len(self.editor.problems), 4)
        self.history.backup()
        self.history.undo()

        self.assertEqual(len(self.editor.problems), 3)
        self.assertEqual(self.editor.next_id, 4)
        self.history.undo()
        self.assertEqual(len(self.editor.problems), 3)
        self.assertEqual(self.editor.next_id, 4)

    def test_undo_then_redo(self):
        problem4 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem4)
        self.history.backup()
        self.history.undo()
        self.history.redo()
        problem  = self.editor.get_problem_by_id(4)

        self.assertEqual(len(self.editor.problems), 4)
        self.assertEqual(self.editor.next_id, 5)
        self.assertEqual(problem.colour, "green")

    def test_undo_then_backup(self):
        problem4 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='green', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        problem5 = Problem(id=4, RIC=RIC(1, 1, 1), grade=Grade('green', 'easy'), colour='orange', sector='tower r', styles=('s',), set_by='s', set_date=datetime.date(2021, 2, 16), strip_date=None)
        self.editor.add_new_problem(problem4)
        self.history.backup()
        self.history.undo()
        self.editor.add_new_problem(problem5)
        self.history.backup()
        problem  = self.editor.get_problem_by_id(4)

        self.assertEqual(len(self.editor.problems), 4)
        self.assertEqual(self.editor.next_id, 5)
        self.assertEqual(problem.colour, "orange")


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