from datetime import date

from services.old_problem_IO import OldProblemIO
from APImodels.grade import Grade
from APImodels.problem import Problem


class OldProblemViewer():
    # interface with GUI to construct user defined filter on stripped problems
    
    _filter_Rs : list[int]
    _filter_Is : list[int]
    _filter_Cs : list[int]
    _filter_grades : list[Grade]
    _filter_setters : list[str]
    _filter_start_date : date
    _filter_end_date : date
    _filter_styles0  : list[str]
    _filter_holds   : list[str]
 
    _repo : OldProblemIO

    def __init__(self, dirIO:OldProblemIO =None):
        self.set_IO_dir(dirIO)
        
    def set_IO_dir(self, dirIO:OldProblemIO) ->None:
        self._repo = dirIO
        if not dirIO is None:
            self._filter_Rs = self.get_risks()
            self._filter_Is = self.get_intensities()
            self._filter_Cs = self.get_complexities()
            self._filter_grades = self.get_grades()
            self._filter_setters = self.get_setters()
            self._filter_start_date = min(self.get_set_dates())
            self._filter_end_date = max(self.get_set_dates())
            self._filter_styles0 = self.get_styles()
            self._filter_holds = self.get_holds()

    def get_risks(self) -> tuple[int,...]:
        # return a list of available risk
        return self._unique((p.RIC.R for p in self._repo.get_all_problems()))

    def get_intensities(self) -> tuple[int,...]:
        # return a list of available intensities
        return self._unique((p.RIC.I for p in self._repo.get_all_problems()))

    def get_complexities(self) -> tuple[int,...]:
        # return a list of available complexities
        return self._unique((p.RIC.C for p in self._repo.get_all_problems()))
    
    def get_grades(self) -> tuple[Grade,...]:
        # return a list of available grades
        return self._unique((p.grade for p in self._repo.get_all_problems()))

    def get_setters(self) -> tuple[str,...]:
        # return a list of available setters
        return self._unique((p.set_by for p in self._repo.get_all_problems()))
    
    def get_set_dates(self) -> tuple[date,...]:
        # return a list of available set dates
        return self._unique((p.set_date for p in self._repo.get_all_problems()))
    
    def get_styles(self) -> tuple[str,...]:
        # return a list of available styles 
        styles = []
        for p in self._repo.get_all_problems():
            styles.extend(list(p.styles))
        return self._unique(styles)

    def get_holds(self) -> tuple[str,...]:
        # return a list of available hold colours
        return self._unique((p.colour for p in self._repo.get_all_problems()))

    def _unique(self, _list:list) -> tuple:
        #return a list of unique values from list
        return tuple(dict.fromkeys(_list).keys())

    def get_filtered_problems(self) -> tuple[Problem,...]:
        return self._repo.filter_problems_by(self._predicate)

    def _predicate(self, problem: Problem) ->bool:
        if self._filter_end_date < self._filter_start_date:
            raise ValueError('End date cannot be before start date')
        return problem.RIC.R in self._filter_Rs and \
        problem.RIC.I in self._filter_Is and \
        problem.RIC.C in self._filter_Cs and \
        problem.grade in self._filter_grades and \
        problem.set_by in self._filter_setters and \
        problem.set_date >= self._filter_start_date and \
        problem.set_date <= self._filter_end_date and \
        problem.colour in self._filter_holds and \
        self._style_in_filter(problem)

    def _style_in_filter(self, problem:Problem) -> bool:
        return len([p for p in problem.styles if p in self._filter_styles0])>0
    
    def set_filter_R(self, value) ->None:
        if isinstance(value, (list,tuple)):
            self._filter_Rs = value

    def set_filter_holds(self, value) ->None:
        if isinstance(value, (list,tuple)):
            self._filter_holds = value
        
    def set_filter_styles(self, value) ->None:
        if isinstance(value, (list,tuple)):
            self._filter_styles0 = value