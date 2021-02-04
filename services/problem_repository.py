

import json

from APImodels.problem import Problem

class ProblemRepository():

    def __init__(self, filepath):
        self.problems = self.__lazy_init(filepath)

    def __lazy_init(self, filepath):
        with open(filepath, 'r') as fid:
            data = json.loads(fid.read())
            result = (Problem.from_json(p) for p in data )
        return result
    
    def get_all_problems(self):
        return self.problems