import unittest
import os

from services.old_problem_IO import OldProblemIO
from APImodels.problem import Problem

class TestOldProblemIO(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.data_dir  = cls._create_dir('data', 'test_old_problems')
        cls.repository = OldProblemIO(cls.data_dir)

    @staticmethod
    def _create_dir(parent:str, folder:str):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, parent,folder)

    def test_init(self):
        problems = self.repository.get_all_problems()
        ids = list([p.id for p in problems])
        ids.sort()
        self.assertListEqual(ids, [9, 10,11,12])

    
    def test_filter(self):
        def predicate(problem:Problem) -> bool:
            return problem.colour == 'purple'

        problems = self.repository.filter_problems_by(predicate)
        ids      = list([p.id for p in problems])
        ids.sort()
        self.assertListEqual(ids, [10,12])