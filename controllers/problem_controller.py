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
    _editor         : ProblemsEditor
    _grade_setting  : GradeDict
    _colour_setting : ColourDict
    _sector_setting : SectorDict

    def __init__(self, dependency:DependencyService, parent=None):
        self._parent = parent
        self._setup_dependencies(dependency)
        self._builder = ProblemAreaDataBuilder(self._grade_setting, self._colour_setting, self._sector_setting)

        self.model = ProblemAreaModel(self._builder.no_problems())   # load model
        self.view  = ProblemArea(self, self.model) # load view
        self._connect_editor()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._grade_setting  = self._dependency.get_or_register(GradeDict)  
        self._colour_setting = self._dependency.get_or_register(ColourDict) 
        self._sector_setting = self._dependency.get_or_register(SectorDict) 
        self._editor         = self._dependency.get(ProblemsEditor)

    def _connect_editor(self):
        self._editor.problemsChanged.connect(self._on_problems_changed)
        self._editor.problemAdded.connect(self._on_problem_added)
        self._editor.problemRemoved.connect(self._on_problem_removed)

    def _on_problems_changed(self, arg:bool):
        # call when the editor notifies that a new set of problems is available and this 
        # set contains all the problems to be shown on screen.
        # To optimise algo, all non-empty cell will be converted either to new data or
        # empty cell. We are expecting about 60 problems on screens at any one time, so
        # at most we only need to convert 120 cells, instead of 247 cells
        
        non_empty_cells = [(c.row, c.col) for c in self.model.data.cells if c.id != 0]
        self.model.changes = self._builder.from_problems(self._editor.problems, tuple(non_empty_cells))

    def _on_problem_added(self, problem:Problem):
        assert(type(problem) == Problem)
        # Call when the editor notifies that a problem is added to that cell. 
        # We only need to change that cell. 
        self.model.changes = self._builder.from_problem(problem)

    def _on_problem_removed(self, problem:Problem):
        # Call when the editor notifies that a problem is removed from that cell. 
        # We only need to change that cell. 
        assert(type(problem) == Problem)
        self.model.changes = self._builder.empty_cell(problem)

    def on_cell_clicked(self, problem_id:int, row:int, col:int) -> bool:
        problem_to_edit     = self._editor.get_problem_by_id(int(problem_id))
        if problem_to_edit is None:
            problem_to_edit = self._make_new_problem(row, col)
        self._editor.problem_to_edit = problem_to_edit
        return True

    def _make_new_problem(self, row:int, col:int):
        # return a new problem with new auto increment id

        _id     = self._editor.next_id
        _grade  = self._grade_setting.get_grade(row)
        _hold   = _grade.split(' ')[0]
        _sector = self._sector_setting.get_sector(col)

        return Problem(_id, RIC(1,1,1), Grade.from_str(_grade), _hold, _sector, (), '', date.today(), 'on')

