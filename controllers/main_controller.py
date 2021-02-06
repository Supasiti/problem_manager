# Main controller
# 
# Aims:
#  - controls interactions with main view
#
from services.dependency_service import DependencyService
from models.main_model import MainModel, MainViewDynamicData
from views.main_window import MainView
from controllers.top_controller import TopController
from controllers.tool_controller import ToolController
from controllers.bottom_controller import BottomController

class MainController():    

    def __init__(self):
        
        self.dependency = DependencyService()
        
        # load other controllers
        self.top_controller = TopController(self.dependency)
        self.bottom_controller = BottomController(self.dependency)
        self.tool_controller = ToolController(self.dependency)

        # build MainViewDynamicData
        view_data = MainViewDynamicData(
            self.top_controller.view, 
            None, 
            self.bottom_controller.view, 
            self.tool_controller.view)

        # load model
        self.model = MainModel(dynamic_data = view_data)

        # load view
        self.view  = MainView(self, self.model)
        self.view.show()
        
        # self.grade_setting  = GradeDict()
        # self.sector_setting = SectorDict()








    # def print_cell_info(self, problem_id):
    #     print('Problem id : %s' % problem_id)

    # def open_directory(self, directory:str):
    #     problem_request = self.dependency.problem_request

    #     self.model.bottom_model.content_path = directory
        
    #     problems = problem_request.get_all_current_problems(directory)
    #     self.model.problem_scroll_area_model.add_problems(problems)
        
    #     sectors = problem_request.get_all_sectors(directory)
    #     self.model.sector_scroll_area_model.sectors = sectors
        