import json

from APImodels.problem import Problem
from APImodels.sector import Sector

class ProblemRepository():
    # manage persistent data for display

    def __init__(self, filepath):
        self.problems = self.__lazy_init(filepath)
        self.sectors  = self.__init_sector()

    def __lazy_init(self, filepath:str):
        with open(filepath, 'r') as fid:
            data = json.loads(fid.read())
            result = (Problem.from_json(p) for p in data )
        return tuple(result)

    def __init_sector(self):
        prob     = self.problems
        if len(prob) == 0: 
            return tuple()
        set_date = self.__get_last_setting_date(prob)
        sectors  = {problem.sector for problem in prob}
        sectors  = tuple(sectors)
        result   = (Sector.from_problems(s, prob, set_date) for s in sectors)
        return tuple(result)

    def __get_last_setting_date(self, problems:tuple):
        prob = tuple(problems)
        if len(prob) == 0: 
            raise ValueError('__get_last_setting_date() don\'t accept empty generator')
        return max([p.set_date for p in prob]) 
     

    def get_all_problems(self):
        return self.problems

    def get_all_sectors(self):
        return self.sectors

    def get_problem_by_id(self, _id:int):
        prob_list = [p for p in self.problems if p.id == _id]
        if len(prob_list) > 0:
            return prob_list[0]
        return None