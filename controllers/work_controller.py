
from models.work_model import WorkStationModel, WorkDynamicData 
from views.work_station import WorkStation
from controllers.problem_controller import ProblemAreaController


class WorkController():
    # controller all interaction the work station

    def __init__(self, dependency):
        self._dependency = dependency
        self.problem_controller = ProblemAreaController(self._dependency) # load other controllers

        view_data  = WorkDynamicData(self.problem_controller.view)
        self.model = WorkStationModel(dynamic_data = view_data) # load model
        self.view  = WorkStation(self, self.model)              # load view
        self.model.dataChanged.connect(self.view.update_UI)