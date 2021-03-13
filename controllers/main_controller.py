from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date

from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor, EditingProblemsEditor, ViewingProblemsEditor
from services.problems_editor_history import ProblemsEditorHistory
from services.sector_editor import SectorEditor
from services.contents_path_manager import ContentsPathManager
from services.json_writer import JsonWriter, StrippedProblemWriter
from services.file_setting import FileSetting
from services.problem_repository import LocalProblemRepository
from services.setting import Setting

from models.main_model import MainModel, MainViewDynamicData
from views.main_window import MainView
from views.dialogs import SaveAsDialog, SaveDialog, WarningDialog
from controllers.top_controller import TopController
from controllers.work_controller import WorkController
from controllers.tool_controller import ToolController, ToolControllerState
from controllers.bottom_controller import BottomController
from controllers.list_view_controller import ProblemListController

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
        self.bottom_controller = BottomController(self._dependency)
        self.top_controller    = TopController(self._dependency)
        self.work_controller   = WorkController(self._dependency)
        self.tool_controller   = ToolController(self._dependency)

        self.model = MainModel(dynamic_data = self._view_data()) # load model
        self.view  = MainView(self, self.model)                  # load view
        self._connect_other()
        self.view.show()
        self.open_current_set()
        
    def _setup_dependencies(self, dependency: DependencyService) -> None:
        self.editor        = ProblemsEditor(EditingProblemsEditor())
        self.history       = ProblemsEditorHistory(self.editor)
        self._dependency   = dependency
        self._dependency.register(ProblemsEditor, self.editor)
        self._dependency.register(ProblemsEditorHistory, self.history)
        self.sector_editor = self._dependency.get(SectorEditor)
        self.path_manager = self._dependency.get(ContentsPathManager)
        self._repo        = self._dependency.get(LocalProblemRepository)
        self.writer       = self._dependency.get(JsonWriter)
        self.strip_writer = self._dependency.get(StrippedProblemWriter)
        # self._setup_editors()

    def change_to_state(self, state:MainControllerState) -> None:
        self._state = state
        self._state.context = self

    def _view_data(self) -> MainViewDynamicData:
        return MainViewDynamicData(self.top_controller.view, self.work_controller.view, self.bottom_controller.view, self.tool_controller.view)
    
    def _connect_other(self) -> None:
        Setting.settingChanged.connect(self._on_setting_changed)
        self.editor.stateChanged.connect(self._on_state_changed)

    def _on_setting_changed(self, class_type:type) -> None:
        if class_type == FileSetting:
            self._open_directory()
    
    def _on_state_changed(self, state_name:str) -> None:
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

    def undo_editing(self) -> None:
        self._state.undo_editing()
    
    def redo_editing(self) -> None:
        self._state.redo_editing()

    def open_current_set(self) -> None:
        if type(self.work_controller) == ProblemListController:
            self._update_work_controller(WorkController(self._dependency))
        self._open_directory()
    
    def _setup_editors(self):
        directory = Setting.get(FileSetting).content_path 
        self.path_manager.directory  = directory
        self._repo.set_filepath(self.path_manager.filepath)
        self.sector_editor.load_sectors(self._repo)
        self.editor.load_problems(self._repo)
        self.editor.change_to_state(EditingProblemsEditor())

    def _open_directory(self) -> None:
        self._setup_editors()
        self.tool_controller.change_to_state(ToolControllerState.Edit)
        self.history.clear()
        self.history.backup()

    def open_previous_set(self) -> None:
        if type(self.work_controller) == ProblemListController:
            self._update_work_controller(WorkController(self._dependency))
        self.editor.change_to_state(ViewingProblemsEditor())   
        self.tool_controller.change_to_state(ToolControllerState.View)

    def open_problem_list_viewer(self) -> None:
        self._update_work_controller(ProblemListController(self._dependency))
        self.change_to_state(ViewingMainController())
        self.tool_controller.change_to_state(ToolControllerState.ListView)

    def _update_work_controller(self, controller) -> None:
        self.work_controller.view.setParent(None)
        self.work_controller = controller
        self.model.dynamic_data = self._view_data()

class MainControllerState(ABC):

    _context     : MainController

    @property
    def context(self) -> MainController:
        return self._context

    @context.setter
    def context(self, context: MainController) -> None:
        self._context = context
    
    @abstractmethod
    def show_save_dialog(self) -> None:
        pass

    @abstractmethod
    def undo_editing(self) -> None:
        pass

    @abstractmethod
    def redo_editing(self) -> None:
        pass

class EditingMainController(MainControllerState):

    def show_save_dialog(self) -> None:
        context = self._context
        dialog = SaveDialog(context.path_manager.filename, self._save_this_set)
        dialog.show()
    
    def _save_this_set(self) -> None:
        path = self._context.path_manager.filepath 
        self._context.writer.set_filepath(path)
        self._set_strip_writer_filepath()
        self._context.editor.save_this_set(self._context.writer, self._context.strip_writer)

    def show_save_as_dialog(self) ->None:
        filename = self._context.top_controller.get_filename()
        dialog  = SaveAsDialog(filename, self._save_as_new_set)
        dialog.show()
    
    def _save_as_new_set(self) -> None:
        is_savable = self._context.top_controller.update_filename_to_save()
        if is_savable:
            path   = self._context.path_manager.filepath_to_save
            self._context.writer.set_filepath(path)
            self._set_strip_writer_filepath()
            self._context.editor.save_this_set(self._context.writer, self._context.strip_writer)
    
    def _set_strip_writer_filepath(self) -> None:
        month_today = date.today().strftime('%Y-%m') # in YYYY-MM
        strip_path  = self._context.path_manager.get_filepath_for_stripped_problem(month_today)
        self._context.strip_writer.set_filepath(strip_path)

    def undo_editing(self) -> None:
        self._context.history.undo()

    def redo_editing(self) -> None:
        self._context.history.redo()

class ViewingMainController(MainControllerState):

    def show_save_dialog(self) ->None:
        dialog = WarningDialog('Save the current set?', 
            'You cannot save the current set in "View" mode.')
        dialog.show()

    def show_save_as_dialog(self) -> None:
        dialog = WarningDialog('Save the current set as new set?', 
            'You cannot save the current set in "View" mode.')
        dialog.show()

    def undo_editing(self) -> None:
        pass

    def redo_editing(self) -> None:
        pass