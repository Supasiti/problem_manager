import json
import os 

from APImodels.problem import Problem

class ProblemRepository():
    # manage persistent data for display

    def __init__(self, filepath):
        self.problems = self._lazy_init(filepath)

    def _lazy_init(self, filepath:str):
        if os.path.getsize(filepath) == 0:
            return tuple() 
        with open(filepath, 'r') as fid:
            data = json.loads(fid.read())
            result = (Problem.from_json(p) for p in data )
        return tuple(result)

    def get_all_problems(self):
        return self.problems

    def get_problem_by_id(self, _id:int):
        prob_list = [p for p in self.problems if p.id == _id]
        if len(prob_list) > 0:
            return prob_list[0]
        return None