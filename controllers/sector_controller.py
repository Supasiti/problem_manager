
from services.problems_editor import ProblemsEditor
from services.dependency_service import DependencyService
from models.sector_area_model import SectorAreaModel, SectorAreaDataBuilder  
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    _dependency : DependencyService

    def __init__(self, dependency : DependencyService, parent=None):
        self._parent  = parent
        self._setup_dependencies(dependency)
        self._builder = SectorAreaDataBuilder()
        self.model    = SectorAreaModel()               # load model
        self.view     = SectorArea(self, self.model)    # load view
        self._connect_editor()
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency

    def _connect_editor(self):
        editor = self._dependency.get(ProblemsEditor)
        editor.problemsChanged.connect(self._on_problems_changed)
        editor.problemAdded.connect(self._on_problems_changed)
        editor.problemRemoved.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        editor    = self._dependency.get(ProblemsEditor)
        self.model.problems_changed(editor.problems)

