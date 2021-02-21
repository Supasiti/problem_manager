import json
import os 

from APImodels.problem import Problem

class ProblemRepository():
    # read .json file with current problem data

    _data    : dict
    _problems : tuple[Problem,...]
    _next_id  : int

    def __init__(self, filepath):
        self._lazy_init(filepath)   
        
    def _lazy_init(self, filepath:str):
        if os.path.getsize(filepath) == 0:
            self._data    = None
            self._next_id  = 0
            self._problems = None
        else:
            with open(filepath, 'r') as fid:
                self._data = json.loads(fid.read())
            self._next_id  = self._data.pop('next_id')
            self._problems = tuple((Problem.from_json(p) for p in self._data.values()))

    @property    
    def next_id(self) -> int:
        return self._next_id

    def get_all_problems(self):
        return self._problems

    def get_problem_by_id(self, _id:int):
        assert(type(_id) == int)
        prob_list = [p for p in self._problems if p.id == _id]
        if len(prob_list) > 0:
            return prob_list[0]
        return None
