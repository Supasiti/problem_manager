
from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from models.tool_model import ToolStationModel, ToolData 
from controllers.editor_controller import EditorController
from controllers.file_controller import FileController
from views.tool_station import ToolStation

class ToolController():
    # controller all interaction the tool station
    
    _dependency     : DependencyService
    _editor         : ProblemsEditor

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        
        # controllers
        self.editor_controller = EditorController(self._dependency)
        self.file_controller   = FileController(self._dependency)

        view_data = ToolData(
            280,
            self.editor_controller.view,
            self.file_controller.view
        )
        self.model = ToolStationModel(view_data = view_data) # load model
        self.view  = ToolStation(self, self.model)           # load view

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)


