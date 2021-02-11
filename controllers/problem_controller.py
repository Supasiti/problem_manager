from services.problem_request import ProblemRequest
from services.dependency_service import DependencyService
from models.problem_area_model import ProblemAreaModel, ProblemAreaDataBuilder 
from models.dicts import GradeDict, SectorDict, ColourDict
from views.scroll_area import ProblemArea

class ProblemAreaController():
    # controller all interaction the top station

    dependency : DependencyService
    grade_setting : GradeDict
    colour_setting : ColourDict
    sector_setting : SectorDict

    def __init__(self, dependency:DependencyService, parent):
        self.__parent = parent
        self.__setup_dependencies(dependency)

        self.builder = ProblemAreaDataBuilder(
                        self.grade_setting, self.colour_setting, self.sector_setting)
        view_data = self.builder.no_problems()

        self.model = ProblemAreaModel(view_data)   # load model
        self.view  = ProblemArea(self, self.model) # load view

    def __setup_dependencies(self, dependency:DependencyService):
        self.dependency = dependency
        self.grade_setting = self.dependency.get_or_register(GradeDict)  
        self.colour_setting = self.dependency.get_or_register(ColourDict) 
        self.sector_setting = self.dependency.get_or_register(SectorDict) 

    def update_all_cells(self, directory:str):
        # update every problem cell when get new list of problems from database 
        problem_request = self.dependency.get(ProblemRequest)
        problems = problem_request.get_all_current_problems(directory)
        view_data = self.builder.build_from_problems(problems)
        self.model.changes = view_data
        
    def on_cell_clicked(self, problem_id:int, row:int, col:int):
        
        if problem_id != 0:
            problem_request = self.dependency.get(ProblemRequest)
            result = problem_request.get_problem_by_id(problem_id)
            if not result is None:
                self.__parent.on_problem_cell_clicked(result)
                return True
        # use row and col to make a new problem
            # self.model.
        print(' to do ')
        # self.__parent.on_problem_cell_clicked(result)
        return True