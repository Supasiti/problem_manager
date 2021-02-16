# Main controller
# 
# Aims:
#  - controls interactions with main view
#
from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from services.path_builder import PathBuilder
from services.contents_path_manager import ContentsPathManager
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
        self._dependency.register(ProblemsEditor)
        self._dependency.register(ContentsPathManager)

        # load other controllers
        self.top_controller    = TopController(self._dependency)
        self.work_controller   = WorkController(self._dependency)
        self.bottom_controller = BottomController(self._dependency)
        self.tool_controller   = ToolController(self._dependency)

        # build MainViewDynamicData
        view_data = MainViewDynamicData(
            self.top_controller.view, 
            self.work_controller.view, 
            self.bottom_controller.view, 
            self.tool_controller.view)

        self.model = MainModel(dynamic_data = view_data) # load model
        self.view  = MainView(self, self.model)          # load view
        self.view.show()
    
    def save_as_new_set(self):
        is_savable = self.top_controller.update_filename_to_save()
        if is_savable:
            editor = self._dependency.get(ProblemsEditor)
            editor.save_as_new_set()
    
    def show_save_as_dialog(self):
        filename = self.top_controller.get_filename()
        dialog = SaveAsDialog(filename, self.save_as_new_set)
        dialog.show()

    def show_save_dialog(self):
        editor           = self._dependency.get(ProblemsEditor)
        builder          = self._dependency.get(PathBuilder)
        current_filename = builder.get_filename(editor.filepath)
        dialog = SaveDialog(current_filename, editor.save_this_set)
        dialog.show()
    
    def open_current_set(self):
        self.bottom_controller.open_directory()
  