from models.tool_model import ToolStationModel 
from views.tool_station import ToolStation

class ToolController():
    # controller all interaction the tool station

    def __init__(self, dependency, parent):
        self.__parent   = parent
        self.dependency = dependency
        
        # load other controllers

        self.model = ToolStationModel()            # load model
        self.view  = ToolStation(self, self.model) # load view