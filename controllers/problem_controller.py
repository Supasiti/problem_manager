from datetime import date
from typing import List

from services.problem_request import ProblemRequest
from services.dependency_service import DependencyService
from models.problem_area_model import ProblemAreaModel, ProblemAreaDataBuilder 
from models.dicts import GradeDict, SectorDict, ColourDict
from views.scroll_area import ProblemArea
from APImodels.grade import Grade
from APImodels.RIC import RIC
from APImodels.problem import Problem


class ProblemAreaController():
    # controller all interaction the top station

    _dependency     : DependencyService
    _grade_setting  : GradeDict
    _colour_setting : ColourDict
    _sector_setting : SectorDict
    _problems       : List[Problem]

    def __init__(self, dependency:DependencyService, parent):
        self._parent = parent
        self._setup_dependencies(dependency)
        self.builder = ProblemAreaDataBuilder(self._grade_setting, self._colour_setting, self._sector_setting)
        view_data    = self.builder.no_problems()

        self.model = ProblemAreaModel(view_data)   # load model
        self.view  = ProblemArea(self, self.model) # load view

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._grade_setting = self._dependency.get_or_register(GradeDict)  
        self._colour_setting = self._dependency.get_or_register(ColourDict) 
        self._sector_setting = self._dependency.get_or_register(SectorDict) 

    def update_all_cells(self, directory:str):
        # update every problem cell when get new list of problems from database 
        problem_request = self._dependency.get(ProblemRequest)
        self._problems  = problem_request.get_all_current_problems(directory)
        view_data = self.builder.build_from_problems(self._problems)
        self.model.changes = view_data
        
    def on_cell_clicked(self, problem_id:int, row:int, col:int) -> bool:
        _problems = [p for p in self._problems if p.id == problem_id]
        result    = _problems[0] if len(_problems) > 0 else self._make_new_problem(row, col)
        self._parent.on_problem_cell_clicked(result)
        return True

    def _make_new_problem(self, row:int, col:int):
        # return a new problem with new auto increment id
        _id     = max([p.id for p in self._problems]) + 1
        _grade  = self._grade_setting.get_grade(row)
        _hold   = _grade.split(' ')[0]
        _sector = self._sector_setting.get_sector(col)

        return Problem(_id, RIC(1,1,1), Grade.from_str(_grade), _hold, _sector, (), '', date.today(), 'on')

