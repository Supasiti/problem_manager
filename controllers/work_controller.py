from APImodels.problem import Problem
from models.work_model import WorkStationModel, WorkDynamicData 
from views.work_station import WorkStation
from controllers.problem_controller import ProblemAreaController
from controllers.sector_controller import SectorAreaController
from controllers.grade_controller import GradeAreaController

class WorkController():
    # controller all interaction the work station

    def __init__(self, dependency, parent=None):
        self._parent     = parent
        self._dependency = dependency
        
        # load other controllers
        self.sector_controller  = SectorAreaController(self._dependency)
        self.grade_controller   = GradeAreaController(self._dependency)
        self.problem_controller = ProblemAreaController(self._dependency)

        # build view data 
        view_data = WorkDynamicData(
            self.sector_controller.view,
            self.grade_controller.view,
            self.problem_controller.view
        )

        self.model = WorkStationModel(dynamic_data = view_data) # load model
        self.view  = WorkStation(self, self.model)              # load view
    

