
from models.bottom_model import BottomStationModel 
from views.bottom_station import BottomStation
from services.problem_request import ProblemRequest

class BottomController():
    # controller all interaction the bottom station

    def __init__(self, dependency, parent):
        self._parent   = parent
        self._dependency = dependency
        
        # load other controllers

        self.model = BottomStationModel()            # load model
        self.view  = BottomStation(self, self.model) # load view
        self.open_directory(self.model.dynamic_data) 

    def open_directory(self, directory:str):
        self.model.dynamic_data = directory
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.get_problems_from_directory(directory)
        # self._parent.on_content_path_changed(directory)
