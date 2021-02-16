# Main controller
# 
# Aims:
#  - controls interactions with main view
#
from services.dependency_service import DependencyService
from services.problem_request import ProblemRequest
from services.path_builder import PathBuilder
from models.main_model import MainModel, MainViewDynamicData
from views.main_window import MainView
from views.dialogs import SaveAsDialog, SaveDialog
from controllers.top_controller import TopController
from controllers.work_controller import WorkController
from controllers.tool_controller import ToolController
from controllers.bottom_controller import BottomController

class MainController():    

    def __init__(self, dependency:DependencyService):
        
        self._dependency = dependency
        self._dependency.register(ProblemRequest)

        # load other controllers
        self.top_controller = TopController(self._dependency, self)
        self.work_controller = WorkController(self._dependency, self)
        self.bottom_controller = BottomController(self._dependency, self)
        self.tool_controller = ToolController(self._dependency, self)

        # build MainViewDynamicData
        view_data = MainViewDynamicData(
            self.top_controller.view, 
            self.work_controller.view, 
            self.bottom_controller.view, 
            self.tool_controller.view)

        self.model = MainModel(dynamic_data = view_data) # load model
        self.view  = MainView(self, self.model)   # load view
        self.view.show()
    
    def save_as_new_set(self):
        is_savable = self.top_controller.update_filename_to_save()
        if is_savable:
            problem_request = self._dependency.get(ProblemRequest)
            problem_request.save_as_new_set()
    
    def show_save_as_dialog(self):
        filename = self.top_controller.get_filename()
        dialog = SaveAsDialog(filename, self.save_as_new_set)
        dialog.show()

    def show_save_dialog(self):
        problem_request  = self._dependency.get(ProblemRequest)
        builder          = self._dependency.get(PathBuilder)
        current_filename = builder.get_filename(problem_request.filepath)
        dialog = SaveDialog(current_filename, problem_request.save_this_set)
        dialog.show()