# Main controller
# 
# Aims:
#  - controls interactions with main view
#
from services.dependency_service import DependencyService
from models.main_model import MainModel, MainViewDynamicData
from views.main_window import MainView
from controllers.top_controller import TopController
from controllers.work_controller import WorkController
from controllers.tool_controller import ToolController
from controllers.bottom_controller import BottomController

class MainController():    

    def __init__(self):
        
        self.dependency = DependencyService()
        
        # load other controllers
        self.top_controller = TopController(self.dependency, self)
        self.work_controller = WorkController(self.dependency, self)
        self.bottom_controller = BottomController(self.dependency, self)
        self.tool_controller = ToolController(self.dependency, self)

        # build MainViewDynamicData
        view_data = MainViewDynamicData(
            self.top_controller.view, 
            self.work_controller.view, 
            self.bottom_controller.view, 
            self.tool_controller.view)

        # load model
        self.model = MainModel(dynamic_data = view_data)

        # load view
        self.view  = MainView(self, self.model)
        self.view.show()
    
    def on_content_path_changed(self, directory:str):
        # call when content path changes
        self.work_controller.on_content_path_changed(directory)



    # def print_cell_info(self, problem_id):
    #     print('Problem id : %s' % problem_id)

