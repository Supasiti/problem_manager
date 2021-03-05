from datetime import date

from services.problems_editor import ProblemsEditor
from services.dependency_service import DependencyService
from services.setting import Setting
from services.grade_setting import GradeSetting
from services.sector_setting import SectorSetting
from models.problem_area_model import ProblemAreaModel, ProblemAreaPanelData, InfoCellModel
from views.scroll_area import ProblemArea
from views.label import InfoCell
from controllers.sector_controller import SectorAreaController
from controllers.grade_controller import GradeAreaController
from APImodels.RIC import RIC
from APImodels.problem import Problem

class ProblemAreaController():
    # controller all interaction the top station

    _dependency     : DependencyService
    _editor         : ProblemsEditor

    def __init__(self, dependency:DependencyService):
        self._setup_dependencies(dependency)

        self.sector_controller = SectorAreaController(self._dependency)
        self.grade_controller  = GradeAreaController(self._dependency)
        self.info_controller   = InfoController(self._dependency)

        self.model   = ProblemAreaModel(self._view_data())            # load model
        self.view    = ProblemArea(self, self.model) # load view
        self._connect()

    def _view_data(self) -> ProblemAreaPanelData:
        return ProblemAreaPanelData(
            self.info_controller.view, 
            self.sector_controller.view,
            self.grade_controller.view
        )

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)

    def _connect(self):
        self.model.cellsChanged.connect(self.view.set_cell_data)
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


class InfoController():

    def __init__(self, dependency:DependencyService):
        self._setup_dependencies(dependency)
        self.model   = InfoCellModel()            # load model
        self.view    = InfoCell(self, self.model) # load view
        self._connect()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)

    def _connect(self) -> None:
        self.model.countsChanged.connect(self.view.set_count)
        self.model.aimChanged.connect(self.view.set_aim)
        self._editor.problemsChanged.connect(self._on_problems_changed)
        self._editor.problemAdded.connect(self._on_problems_changed)
        self._editor.problemRemoved.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool) -> None:
        self.model.counts = len(self._editor.problems)
