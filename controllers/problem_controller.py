
from models.problem_area_model import ProblemAreaModel, ProblemAreaDataBuilder 
from models.dicts import GradeDict,SectorDict,ColourDict
from views.scroll_area import ProblemArea

class ProblemAreaController():
    # controller all interaction the top station

    def __init__(self, dependency, parent):
        self.__parent   = parent
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

    def update_all_cells(self, directory:str):
        # update every problem cell when get new list of problems from database 
        problem_request = self.dependency.problem_request
        problems = problem_request.get_all_current_problems(directory)
        view_data = self.builder.build_from_problems(problems)
        self.model.changes = view_data
        