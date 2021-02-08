
from models.grade_area_model import GradeAreaModel, GradeAreaDataBuilder, GradeCountsDataBuilder  
from models.dicts import GradeDict,ColourDict
from views.scroll_area import GradeArea

class GradeAreaController():
    # controller all interaction the top station

    def __init__(self, dependency, parent):
        self.__parent   = parent
        self.dependency = dependency
        self.colour_setting = ColourDict()
        self.grade_setting = GradeDict()

        # build data
        self.builder = GradeAreaDataBuilder(
                        self.grade_setting, self.colour_setting)
        self.count_builder = GradeCountsDataBuilder(
                        self.grade_setting, self.colour_setting)             
        data = self.builder.default()
        counts = self.count_builder.default()

        self.model = GradeAreaModel(data, counts)   # load model
        self.view  = GradeArea(self, self.model) # load view
    
    # def update_all_cells(self, directory:str):
    #     # update every sector cell when get new list of problems from database 
    #     problem_request = self.dependency.problem_request
    #     sectors = problem_request.get_all_sectors(directory)
    #     view_data = self.builder.build_from_sectors(sectors)
    #     self.model.changes = view_data
