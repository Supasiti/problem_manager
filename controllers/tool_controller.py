from services.dependency_service import DependencyService
from services.problem_request import ProblemRequest
from models.tool_model import ToolStationModel, ToolDynamicData 
from models.dicts import ColourDict
from views.tool_station import ToolStation

from APImodels.problem import Problem


class ToolController():
    # controller all interaction the tool station

    def __init__(self, dependency: DependencyService, parent:object):
        self.__parent   = parent
        self.dependency = dependency
        self.colour_setting = self.dependency.get_or_register(ColourDict)
        
        view_data = self.__default_view_data()

        self.model = ToolStationModel(dynamic_data=view_data) # load model
        self.view  = ToolStation(self, self.model) # load view

    def __default_view_data(self):
        problem   = Problem()
        grade_str = str(problem.grade)
        holds     = self.colour_setting.get_hold_colours(grade_str)
        return ToolDynamicData(holds, problem)

    def update_from_cell_area(self, problem_id:int, row:int, col:int ):

        if problem_id == 0:
            print('row: %s, col %s' % (row, col)) # will need to change this later
            return True
        problem_request = self.dependency.get(ProblemRequest)
        problem = problem_request.get_problem_by_id(problem_id)
        if problem is None :
            print('row: %s, col %s' % (row, col))
            return True
        grade_str = str(problem.grade)
        holds     = self.colour_setting.get_hold_colours(grade_str)
        self.model.dynamic_data = ToolDynamicData(holds, problem)
        