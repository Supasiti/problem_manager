from datetime import date

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

    dependency : DependencyService
    grade_setting : GradeDict
    colour_setting : ColourDict
    sector_setting : SectorDict

    def __init__(self, dependency:DependencyService, parent):
        self._parent = parent
        self._setup_dependencies(dependency)

        self.builder = ProblemAreaDataBuilder(
                        self.grade_setting, self.colour_setting, self.sector_setting)
        view_data = self.builder.no_problems()

        self.model = ProblemAreaModel(view_data)   # load model
        self.view  = ProblemArea(self, self.model) # load view

    def _setup_dependencies(self, dependency:DependencyService):
        self.dependency = dependency
        self.grade_setting = self.dependency.get_or_register(GradeDict)  
        self.colour_setting = self.dependency.get_or_register(ColourDict) 
        self.sector_setting = self.dependency.get_or_register(SectorDict) 

    def update_all_cells(self, directory:str):
        # update every problem cell when get new list of problems from database 
        problem_request = self.dependency.get(ProblemRequest)
        problems = problem_request.get_all_current_problems(directory)
        view_data = self.builder.build_from_problems(problems)
        self.model.changes = view_data
        
    def on_cell_clicked(self, problem_id:int, row:int, col:int):
        
        if problem_id != 0:
            problem_request = self.dependency.get(ProblemRequest)
            result = problem_request.get_problem_by_id(problem_id)
            if not result is None:
                self._parent.on_problem_cell_clicked(result)
                return True
        _new_problem = self._make_new_problem(row, col)
        self._parent.on_problem_cell_clicked(_new_problem)
        return True

    def _make_new_problem(self, row:int, col:int):
        # return a new problem with new auto increment id
        _id     = max([p.id for p in self.model.data.cells]) + 1
        _grade  = self.grade_setting.get_grade(row)
        _hold   = _grade.split(' ')[0]
        _sector = self.sector_setting.get_sector(col)

        return Problem(_id, RIC(1,1,1), Grade.from_str(_grade), _hold, _sector, (), '', date.today(), 'on')

    