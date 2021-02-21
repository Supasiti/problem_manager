import json
import os 

from APImodels.problem import Problem

class ProblemRepository():
    # read .json file with current problem data

    _data    : dict
    problems : tuple[Problem,...]
    next_id  : int

    def __init__(self, filepath):
        self._lazy_init(filepath)   
        
    def _lazy_init(self, filepath:str):
        if os.path.getsize(filepath) == 0:
            self._data    = None
            self.next_id  = 0
            self.problems = None
        else:
            with open(filepath, 'r') as fid:
                self._data = json.loads(fid.read())
            self.next_id  = self._data.pop('next_id')
            self.problems = tuple((Problem.from_json(p) for p in self._data.values()))
        

    def get_all_problems(self):
        return self.problems

    def get_problem_by_id(self, _id:int):
        assert(type(_id) == int)
        prob_list = [p for p in self.problems if p.id == _id]
        if len(prob_list) > 0:
            return prob_list[0]
        return None
