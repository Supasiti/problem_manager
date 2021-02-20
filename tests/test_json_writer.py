import unittest
import os

from services.problem_repository import ProblemRepository
from services.json_writer import JsonWriter

class TestJsonWriter(unittest.TestCase):

    def setUp(self):
        self.data_filepath  = self._create_filepath('data',     'test_problems_data.json')
        self.write_filepath = self._create_filepath('write_to', 'test_json_write_to.json')
        self.repository = ProblemRepository(self.data_filepath)
        self.problems   =  self.repository.get_all_problems()
        self.writer     = JsonWriter(self.write_filepath, self.problems)

    def _create_filepath(self, folder:str, filename:str):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, folder,filename)

    def test_write(self):

        self.writer.write()
        read_repo = ProblemRepository(self.write_filepath)
        problems  = read_repo.get_all_problems()
        
        for problem in problems:
            original = [p for p in self.problems if p.id == problem.id ][0]
            self.assertEqual(problem, original)