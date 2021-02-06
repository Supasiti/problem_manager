
from models.top_model import TopStationModel 
from views.top_station import TopStation

class TopController():
    # controller all interaction the top station

    def __init__(self, dependency):
        
        self.dependency = dependency
        
        # load other controllers

        self.model = TopStationModel()            # load model
        self.view  = TopStation(self, self.model) # load view
