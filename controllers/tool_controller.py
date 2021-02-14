from services.dependency_service import DependencyService
from services.problem_request import ProblemRequest
from models.tool_model import ToolStationModel, ToolDynamicData 
from models.dicts import ColourDict
from views.tool_station import ToolStation

from APImodels.problem import Problem


class ToolController():
    # controller all interaction the tool station

    def __init__(self, dependency: DependencyService, parent:object):
        self._parent         = parent
        self._dependency     = dependency
        self._colour_setting = self._dependency.get_or_register(ColourDict)
        
        view_data  = self._default_view_data()
        self.model = ToolStationModel(dynamic_data = view_data) # load model
        self.view  = ToolStation(self, self.model)              # load view
        self._connect_problem_request()

    def _default_view_data(self):
        problem   = Problem()
        grade_str = str(problem.grade)
        holds     = self._colour_setting.get_hold_colours(grade_str)
        return ToolDynamicData(holds, problem)

    def _connect_problem_request(self):
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.problemToEditChanged.connect(self._on_problem_to_edit_changed)

    def _on_problem_to_edit_changed(self, arg:bool):
        problem_request = self._dependency.get(ProblemRequest)
        problem_to_edit = problem_request.problem_to_edit
        if not problem_to_edit is None:
            self._update_view(problem_to_edit)
            return True
        self.model.dynamic_data = self._default_view_data()
        return True

    def _update_view(self, problem:Problem):
        grade_str = str(problem.grade)
        holds     = self._colour_setting.get_hold_colours(grade_str)
        self.model.dynamic_data = ToolDynamicData(holds, problem)
        return True