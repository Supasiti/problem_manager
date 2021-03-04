from datetime import date

from services.problems_editor import ProblemsEditor
from services.dependency_service import DependencyService
from services.setting import Setting
from services.grade_setting import GradeSetting

from services.sector_setting import SectorSetting
from models.problem_area_model import ProblemAreaModel
from views.scroll_area import ProblemArea
from APImodels.RIC import RIC
from APImodels.problem import Problem

class ProblemAreaController():
    # controller all interaction the top station

    _dependency     : DependencyService
    _editor         : ProblemsEditor

    def __init__(self, dependency:DependencyService, parent=None):
        self._parent = parent
        self._setup_dependencies(dependency)
        self.model   = ProblemAreaModel()   # load model
        self.view    = ProblemArea(self, self.model)                   # load view
        self._connect_editor()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)

    def _connect_editor(self):
        self._editor.problemsChanged.connect(self._on_problems_changed)
        self._editor.problemAdded.connect(self._on_problem_added)
        self._editor.problemRemoved.connect(self._on_problem_removed)

    def _on_problems_changed(self, arg:bool):
        self.model.update_problems(self._editor.problems)
        
    def _on_problem_added(self, problem:Problem):
        self.model.add_problem(problem)

    def _on_problem_removed(self, problem:Problem):
        self.model.remove_problem(problem)

    def on_cell_clicked(self, problem_id:int, row:int, col:int) -> bool:
        problem_to_edit     = self._editor.get_problem_by_id(int(problem_id))
        if problem_to_edit is None:
            problem_to_edit = self._make_new_problem(row, col)
        self._editor.problem_to_edit = problem_to_edit
        return True

    def _make_new_problem(self, row:int, col:int):
        # return a new problem with new auto increment id

        _id     = self._editor.next_id
        _grade  = Setting.get(GradeSetting).get_grade(row)
        _hold   = str(_grade).split(' ')[0]
        _sector = Setting.get(SectorSetting).get_sector(col)

        return Problem(_id, RIC(1,1,1), _grade, _hold, _sector, (), '', date.today(), 'on')

