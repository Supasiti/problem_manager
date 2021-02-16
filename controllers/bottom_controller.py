
from models.bottom_model import BottomStationModel 
from views.bottom_station import BottomStation
from services.problems_editor import ProblemsEditor

class BottomController():
    # controller all interaction the bottom station

    def __init__(self, dependency, parent=None):
        self._parent   = parent
        self._dependency = dependency
        
        # load other controllers

        self.model = BottomStationModel()            # load model
        self.view  = BottomStation(self, self.model) # load view
        self.open_directory(self.model.dynamic_data) 

    def open_directory(self, directory:str =None):
        if directory is None:
            directory = self.get_directory()
        self.model.dynamic_data = directory
        editor = self._dependency.get(ProblemsEditor)
        editor.open_directory(directory)

    def get_directory(self):
        return self.view.path_info.text()