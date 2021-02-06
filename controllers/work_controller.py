
from models.work_model import WorkStationModel, WorkDynamicData 
from views.work_station import WorkStation
from controllers.problem_controller import ProblemAreaController
from controllers.sector_controller import SectorAreaController

class WorkController():
    # controller all interaction the work station

    def __init__(self, dependency):
        
        self.dependency = dependency
        
        # load other controllers
        # self.info_controller    = None
        self.sector_controller = SectorAreaController(self.dependency)
        self.problem_controller = ProblemAreaController(self.dependency)

        # build view data 
        view_data = WorkDynamicData(
            None,
            self.sector_controller.view,
            None,
            self.problem_controller.view
        )

        self.model = WorkStationModel(dynamic_data = view_data) # load model
        self.view  = WorkStation(self, self.model) # load view