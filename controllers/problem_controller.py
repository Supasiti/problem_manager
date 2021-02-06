
from models.problem_area_model import ProblemAreaModel, ProblemAreaDataBuilder 
from models.dicts import GradeDict,SectorDict,ColourDict
from views.scroll_area import ProblemArea

class ProblemAreaController():
    # controller all interaction the top station

    def __init__(self, dependency):
        
        self.dependency = dependency
        self.grade_setting  = GradeDict()
        self.colour_setting = ColourDict()
        self.sector_setting = SectorDict()

        # build data
        self.builder = ProblemAreaDataBuilder(
                        self.grade_setting, self.colour_setting, self.sector_setting)
        view_data = self.builder.no_problems()

        self.model = ProblemAreaModel(view_data)   # load model
        self.view  = ProblemArea(self, self.model) # load view
