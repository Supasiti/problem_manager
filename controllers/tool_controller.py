from __future__ import annotations 
from enum import Enum

from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from models.tool_model import ToolStationModel
from controllers.editor_controller import EditorController
from controllers.file_controller import FileController
from controllers.filter_controller import FilterController
from views.tool_station import ToolStation

class ToolControllerState(Enum):

    Edit     = 1
    View     = 2
    ListView = 3

class ToolController():
    # controller all interaction the tool station
    
    _dependency     : DependencyService
    _editor         : ProblemsEditor
    _controllers = tuple() 
    _state_dict  = {
        ToolControllerState.Edit : (EditorController,),
        ToolControllerState.View : (EditorController, FileController),
        ToolControllerState.ListView : (FilterController,)
    }

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        self.model = ToolStationModel()                # load model
        self.view  = ToolStation(self, self.model)     # load view
        self._connect()
        self.change_to_state(ToolControllerState.Edit)

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)

    def _connect(self) -> None:
        self.model.dataChanged.connect(self.view.set_data)

    def change_to_state(self, state:ToolControllerState) -> None:
        if state in self._state_dict.keys():
            self._remove_current_views()
            self._controllers = tuple([controller(self._dependency) for controller in self._state_dict[state]])
            widgets = (controller.view for controller in self._controllers)
            self.model.set_widgets(widgets)

    def _remove_current_views(self):
        for controller in self._controllers:
            controller.view.setParent(None)