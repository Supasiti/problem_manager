
from services.problem_request import ProblemRequest
from services.dependency_service import DependencyService
from models.sector_area_model import SectorAreaModel, SectorAreaDataBuilder  
from models.dicts import SectorDict,ColourDict
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    dependency : DependencyService
    colour_setting : ColourDict
    sector_setting : SectorDict

    def __init__(self, dependency : DependencyService, parent):
        self.__parent   = parent
        self.__setup_dependencies(dependency)

        self.builder = SectorAreaDataBuilder(
                        self.sector_setting, self.colour_setting)
        view_data = self.builder.default()

        self.model = SectorAreaModel(view_data)   # load model
        self.view  = SectorArea(self, self.model) # load view
    
    def __setup_dependencies(self, dependency:DependencyService):
        self.dependency = dependency
        self.colour_setting = self.dependency.get_or_register(ColourDict) 
        self.sector_setting = self.dependency.get_or_register(SectorDict)

    def update_all_cells(self, directory:str):
        # update every sector cell when get new list of problems from database 
        problem_request = self.dependency.get(ProblemRequest)
        sectors = problem_request.get_all_sectors(directory)
        view_data = self.builder.build_from_sectors(sectors)
        self.model.changes = view_data
