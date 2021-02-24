from __future__ import annotations
from abc import ABC, abstractmethod

from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor, EditingProblemsEditor, ViewingProblemsEditor
from services.contents_path_manager import ContentsPathManager
from services.json_writer import JsonWriter
from models.main_model import MainModel, MainViewDynamicData
from views.main_window import MainView
from views.dialogs import SaveAsDialog, SaveDialog, WarningDialog
from controllers.top_controller import TopController
from controllers.work_controller import WorkController
from controllers.tool_controller import ToolController
from controllers.bottom_controller import BottomController

class MainController():    
# Aims:
#  - controls interactions with main view

    _dependency   : DependencyService
    _state        : MainControllerState
    editor        : ProblemsEditor
    path_manager  : ContentsPathManager

    def __init__(self, dependency:DependencyService):
        self._setup_dependencies(dependency)
        self.change_to_state(EditingMainController())

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
        self._connect_other()
    
    def _setup_dependencies(self, dependency: DependencyService):
        self.editor        = ProblemsEditor(EditingProblemsEditor())
        self._dependency   = dependency
        self._dependency.register(ProblemsEditor, self.editor)
        self.path_manager = self._dependency.get(ContentsPathManager)
        self.writer       = self._dependency.get(JsonWriter)

    def change_to_state(self, state:MainControllerState):
        self._state = state
        self._state.context = self

    def _connect_other(self):
        self.editor.stateChanged.connect(self._on_state_changed)
    
    def _on_state_changed(self, state_name:str):
        if state_name == 'editing':
            self.change_to_state(EditingMainController())
        elif state_name == 'viewing':
            self.change_to_state(ViewingMainController())
        else:
            raise ValueError('Main Controller: incorrect state name')
    
    def show_save_as_dialog(self):
        self._state.show_save_as_dialog()

    def show_save_dialog(self):
        self._state.show_save_dialog()

    def open_current_set(self):
        self.editor.change_to_state(EditingProblemsEditor())
        self.bottom_controller.open_directory()
  
    def open_previous_set(self):
        self.editor.change_to_state(ViewingProblemsEditor())
        # do something


class MainControllerState(ABC):

    _context     : MainController

    @property
    def context(self) -> MainController:
        return self._context

    @context.setter
    def context(self, context: MainController) -> None:
        self._context = context
    
    @abstractmethod
    def show_save_dialog(self):
        pass

class EditingMainController(MainControllerState):

    def show_save_dialog(self):
        context = self._context
        dialog = SaveDialog(context.path_manager.filename, self._save_this_set)
        dialog.show()
    
    def _save_this_set(self):
        path = self._context.path_manager.filepath 
        self._context.writer.set_filepath(path)
        self._context.editor.save_this_set(self._context.writer)

    def show_save_as_dialog(self):
        filename = self._context.top_controller.get_filename()
        dialog  = SaveAsDialog(filename, self._save_as_new_set)
        dialog.show()
    
    def _save_as_new_set(self):
        is_savable = self._context.top_controller.update_filename_to_save()
        if is_savable:
            path   = self._context.path_manager.filepath_to_save
            self._context.writer.set_filepath(path)
            self._context.editor.save_this_set(self._context.writer)

class ViewingMainController(MainControllerState):

    def show_save_dialog(self):
        dialog = WarningDialog('Save the current set?', 
            'You cannot save the current set in "View" mode.')
        dialog.show()

    def show_save_as_dialog(self):
        dialog = WarningDialog('Save the current set as new set?', 
            'You cannot save the current set in "View" mode.')
        dialog.show()