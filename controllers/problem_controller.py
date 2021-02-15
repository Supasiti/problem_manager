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

    _dependency     : DependencyService
    _grade_setting  : GradeDict
    _colour_setting : ColourDict
    _sector_setting : SectorDict

    def __init__(self, dependency:DependencyService, parent):
        self._parent = parent
        self._setup_dependencies(dependency)
        self.builder = ProblemAreaDataBuilder(self._grade_setting, self._colour_setting, self._sector_setting)
        view_data    = self.builder.no_problems()

        self.model = ProblemAreaModel(view_data)   # load model
        self.view  = ProblemArea(self, self.model) # load view
        self._connect_problem_request()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._grade_setting = self._dependency.get_or_register(GradeDict)  
        self._colour_setting = self._dependency.get_or_register(ColourDict) 
        self._sector_setting = self._dependency.get_or_register(SectorDict) 

    def _connect_problem_request(self):
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.problemsChanged.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        problem_request    = self._dependency.get(ProblemRequest)
        problems           = problem_request.problems
        view_data          = self.builder.build_from_problems(problems)
        self.model.changes = view_data
        
    def on_cell_clicked(self, problem_id:int, row:int, col:int) -> bool:
        problem_request     = self._dependency.get(ProblemRequest)
        problem_to_edit     = problem_request.get_problem_by_id(int(problem_id))
        if problem_to_edit is None:
            problem_to_edit = self._make_new_problem(row, col)
        problem_request.problem_to_edit = problem_to_edit
        return True

    def _make_new_problem(self, row:int, col:int):
        # return a new problem with new auto increment id
        problem_request = self._dependency.get(ProblemRequest)

        _id     = problem_request.next_id
        _grade  = self._grade_setting.get_grade(row)
        _hold   = _grade.split(' ')[0]
        _sector = self._sector_setting.get_sector(col)

        return Problem(_id, RIC(1,1,1), Grade.from_str(_grade), _hold, _sector, (), '', date.today(), 'on')

