
from models.bottom_model import BottomStationModel 
from views.bottom_station import BottomStation

class BottomController():
    # controller all interaction the bottom station

    def __init__(self, dependency, parent):
        self.__parent   = parent
        self.dependency = dependency
        
        # load other controllers

        self.model = BottomStationModel()            # load model
        self.view  = BottomStation(self, self.model) # load view
        self.open_directory(self.model.dynamic_data) 

    def open_directory(self, directory:str):
        self.model.dynamic_data = directory
        self.__parent.on_content_path_changed(directory)
