# Python version 3.9.1
# class containing global information on each climbing sector

from typing import NamedTuple
from datetime import date
from APImodels.problem import Problem

class Sector(NamedTuple):
    name :str
    count : int
    problem_ids : tuple
    setting : bool

    @classmethod
    def from_problems(cls, name:str, problems:tuple, last_set_date:date):
        
        sector_problems = [p for p in problems if p.sector == name]
        count   = len(sector_problems)
        ids     = tuple(int(p.id) for p in sector_problems) if count > 0 else tuple()
        setting = cls._is_setting(tuple(sector_problems), last_set_date)
        return Sector(name, count, ids, setting)

    @staticmethod
    def _is_setting(sector_problems:tuple[Problem,...], last_set_date:date):
        if len(sector_problems) == 0: 
            return False
        return last_set_date in [p.set_date for p in sector_problems]