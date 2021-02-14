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
        
        self.model = ToolStationModel(dynamic_data = self._view_data()) # load model
        self.view  = ToolStation(self, self.model)                      # load view
        self._connect_problem_request()

    def _connect_problem_request(self):
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.problemToEditChanged.connect(self._on_problem_to_edit_changed)

    def _on_problem_to_edit_changed(self, arg:bool):
        problem_request         = self._dependency.get(ProblemRequest)
        problem_to_edit         = problem_request.problem_to_edit
        self.model.dynamic_data = self._view_data(problem_to_edit)
        return True

    def _view_data(self, problem:Problem = None):
        _problem  = Problem() if problem is None else problem
        grade_str = str(_problem.grade)
        holds     = self._colour_setting.get_hold_colours(grade_str)
        return ToolDynamicData(holds, _problem)