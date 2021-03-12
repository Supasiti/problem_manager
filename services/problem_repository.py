from abc import ABC, abstractmethod
import json
import os 

from APImodels.problem import Problem

class ProblemRepository(ABC):

    @property
    @abstractmethod
    def next_id(self) -> int:
        pass
    
    @abstractmethod
    def get_all_problems(self) -> tuple:
        pass

    @abstractmethod
    def get_problem_by_id(self, _id:int) -> Problem:
        pass
    
    @abstractmethod
    def get_all_sectors(self) -> dict:
        pass


class LocalProblemRepository(ProblemRepository):
    # read .json file with current problem data

    _data      : dict
    _filepath  : str
    _problems  : tuple[Problem,...]
    _next_id   : int
    _sectors   : dict

    def __init__(self, filepath =''):
        if filepath !='':
            self.set_filepath(filepath)
    
    def set_filepath(self, filepath:str):
        self._filepath = filepath
        self._lazy_init(filepath)    
    
    def _lazy_init(self, filepath:str):
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            self._data     = dict()
            self._next_id  = 1
            self._problems = tuple()
            self._sectors  = dict()
        else:
            with open(filepath, 'r') as fid:
                self._data = json.loads(fid.read())
            self._next_id  = int(self._data['next_id'])
            self._problems = tuple((Problem.from_json(p) for p in self._data['problems'].values()))
            self._sectors  = self._data['sectors']
    
    @property    
    def next_id(self) -> int:
        return self._next_id

    def get_all_problems(self) ->tuple:
        return self._problems

    def get_problem_by_id(self, _id:int) -> Problem:
        assert(type(_id) == int)
        prob_list = [p for p in self._problems if p.id == _id]
        if len(prob_list) > 0:
            return prob_list[0]
        return None

    def get_all_sectors(self) -> dict:
        return self._sectors.copy()