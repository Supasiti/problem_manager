from datetime import date

from services.problems_editor import ProblemsEditor
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
        self._connect_editor()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._grade_setting = self._dependency.get_or_register(GradeDict)  
        self._colour_setting = self._dependency.get_or_register(ColourDict) 
        self._sector_setting = self._dependency.get_or_register(SectorDict) 

    def _connect_editor(self):
        editor = self._dependency.get(ProblemsEditor)
        editor.problemsChanged.connect(self._on_problems_changed)
        editor.problemAdded.connect(self._on_problem_added)
        editor.problemRemoved.connect(self._on_problem_removed)

    def _on_problems_changed(self, arg:bool):
        editor             = self._dependency.get(ProblemsEditor)
        problems           = editor.problems
        self.model.changes = self.builder.from_problems(problems)

    def _on_problem_added(self, problem:Problem):
        assert(type(problem) == Problem)
        self.model.changes = self.builder.from_problem(problem)

    def _on_problem_removed(self, problem:Problem):
        assert(type(problem) == Problem)
        self.model.changes = self.builder.empty_cell(problem)

    def on_cell_clicked(self, problem_id:int, row:int, col:int) -> bool:
        editor              = self._dependency.get(ProblemsEditor)
        problem_to_edit     = editor.get_problem_by_id(int(problem_id))
        if problem_to_edit is None:
            problem_to_edit = self._make_new_problem(row, col)
        editor.problem_to_edit = problem_to_edit
        return True

    def _make_new_problem(self, row:int, col:int):
        # return a new problem with new auto increment id
        editor  = self._dependency.get(ProblemsEditor)

        _id     = editor.next_id
        _grade  = self._grade_setting.get_grade(row)
        _hold   = _grade.split(' ')[0]
        _sector = self._sector_setting.get_sector(col)

        return Problem(_id, RIC(1,1,1), Grade.from_str(_grade), _hold, _sector, (), '', date.today(), 'on')

