from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor, EditingProblemsEditor, ViewingProblemsEditor
from services.contents_path_manager import ContentsPathManager
from models.main_model import MainModel, MainViewDynamicData
from views.main_window import MainView
from views.dialogs import SaveAsDialog, SaveDialog
from controllers.top_controller import TopController
from controllers.work_controller import WorkController
from controllers.tool_controller import ToolController
from controllers.bottom_controller import BottomController

class MainController():    
# Aims:
#  - controls interactions with main view

    _dependency   : DependencyService
    _editor       : ProblemsEditor
    _path_manager : ContentsPathManager

    def __init__(self, dependency:DependencyService):
        self._setup_dependencies(dependency)

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
    
    def _setup_dependencies(self, dependency: DependencyService):
        self._dependency   = dependency
        self._editor       = ProblemsEditor(EditingProblemsEditor())
        self._dependency.register(ProblemsEditor, self._editor)
        self._path_manager = self._dependency.get_or_register(ContentsPathManager)

    def _save_as_new_set(self):
        is_savable = self.top_controller.update_filename_to_save()
        if is_savable:
            path   = self._path_manager.filepath_to_save
            self._editor.save_as_new_set(path)
    
    def show_save_as_dialog(self):
        filename = self.top_controller.get_filename()
        dialog  = SaveAsDialog(filename, self._save_as_new_set)
        dialog.show()

    def show_save_dialog(self):
        dialog = SaveDialog(self._path_manager.filename, self._save_this_set)
        dialog.show()
    
    def _save_this_set(self):
        path = self._path_manager.filepath  
        self._editor.save_this_set(path)

    def open_current_set(self):
        self._editor.change_to_state(EditingProblemsEditor())
        self.bottom_controller.open_directory()
  
    def open_previous_set(self):
        self._editor.change_to_state(ViewingProblemsEditor())