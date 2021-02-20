import unittest
import os

from services.problem_repository import ProblemRepository
from APImodels.problem import Problem

class TestProblemRepository(unittest.TestCase):

    def setUp(self):
        self.filepath = self._create_filepath('data', 'test_problems_data.json')
        self.repository = ProblemRepository(self.filepath)

    def _create_filepath(self, folder:str, filename:str):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, folder,filename)

    def test_init(self):
        problems = self.repository.get_all_problems()

        self.assertEqual(type(problems), tuple)
        self.assertEqual(len(problems), 3)
        self.assertEqual(type(problems[0]), Problem)

    def test_get_problem_by_id(self):
        problem_1 = self.repository.get_problem_by_id(1)
        problem_4 = self.repository.get_problem_by_id(4)

        self.assertEqual(type(problem_1), Problem)
        self.assertEqual(problem_1.colour, 'red')
        self.assertEqual(problem_4, None)