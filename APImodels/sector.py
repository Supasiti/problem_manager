# Python version 3.9.1
# class containing global information on each climbing sector

from typing import NamedTuple
from datetime import date

class Sector(NamedTuple):
    name :str
    count : int
    problem_ids : tuple
    setting : bool

    def with_new_problem(self, problem_id:int):
        p_set = set(self.problem_ids)
        p_set.add(problem_id)
        new_problem_ids = tuple(p_set)
        new_count = len(new_problem_ids)
        return Sector(self.name, new_count, new_problem_ids, self.setting)

    def with_a_problem_removed(self, problem_id:int):
        p_set = set(self.problem_ids)
        if problem_id in p_set:
            p_set.remove(problem_id)
        new_problem_ids = tuple(p_set)
        new_count = len(new_problem_ids)
        return Sector(self.name, new_count, new_problem_ids, self.setting)

    def with_new_set(self, new_set:str):
        return Sector(self.name, self.count, self.problem_ids, new_set)

    def with_problems_cleared(self):
        return Sector(self.name, 0, tuple(), self.setting)

    @classmethod
    def from_problems(cls, name:str, problems:tuple, last_set_date:date):
        
        sector_problems = [p for p in problems if p.sector == name]
        
        count   = len(sector_problems)
        ids     = tuple(p.id for p in sector_problems)
        setting = cls.__is_setting(tuple(sector_problems), last_set_date)
        return Sector(name, count, ids, setting)

    @staticmethod
    def __is_setting(sector_problems:tuple, last_set_date:date):
        if len(sector_problems) == 0: 
            raise ValueError('__is_setting() don\'t accept empty list')
        return last_set_date in [p.set_date for p in sector_problems]