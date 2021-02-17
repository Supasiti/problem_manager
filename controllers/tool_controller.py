
from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from models.tool_model import ToolStationModel, ToolData 
from models.dicts import ColourDict
from controllers.editor_controller import EditorController
from views.tool_station import ToolStation


class ToolController():
    # controller all interaction the tool station
    
    _dependency     : DependencyService
    _colour_setting : ColourDict
    _editor         : ProblemsEditor

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        
        # controllers
        self.editor_controller = EditorController(self._dependency)

        view_data = ToolData(
            280,
            self.editor_controller.view
        )
        self.model         = ToolStationModel(view_data = view_data) # load model
        self.view          = ToolStation(self, self.model)  # load view
        # self._connect_other()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)

    # def _connect_other(self):
    #     self._editor.stateChanged.connect(self._on_state_changed)


    # def _on_state_changed(self, name:str):
    #     if name == 'editing':
    #         self._is_updatable = True
    #     elif name == 'viewing':
    #         self._is_updatable = False
    #     else:
    #         raise ValueError('incorrect state')
    #     self.model.dynamic_data = self.view_data()

