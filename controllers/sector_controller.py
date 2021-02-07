
from models.sector_area_model import SectorAreaModel, SectorAreaDataBuilder  
from models.dicts import SectorDict,ColourDict
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    def __init__(self, dependency, parent):
        self.__parent   = parent
        self.dependency = dependency
        self.colour_setting = ColourDict()
        self.sector_setting = SectorDict()

        # build data
        self.builder = SectorAreaDataBuilder(
                        self.sector_setting, self.colour_setting)
        view_data = self.builder.default()

        self.model = SectorAreaModel(view_data)   # load model
        self.view  = SectorArea(self, self.model) # load view
    
    def update_all_cells(self, directory:str):
        # update every sector cell when get new list of problems from database 
        problem_request = self.dependency.problem_request
        sectors = problem_request.get_all_sectors(directory)
        view_data = self.builder.build_from_sectors(sectors)
        self.model.changes = view_data
    #     self.model.sector_scroll_area_model.sectors = sectors