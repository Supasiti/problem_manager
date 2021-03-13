
from services.problems_editor import ProblemsEditor
from services.dependency_service import DependencyService
from services.sector_editor import SectorEditor
from models.sector_area_model import SectorAreaModel
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    _dependency : DependencyService

    def __init__(self, dependency : DependencyService):
        self._setup_dependencies(dependency)
        self.model    = SectorAreaModel(self._sector_editor) # load model
        self.view     = SectorArea(self, self.model)         # load view
        self._connect()
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._sector_editor = self._dependency.get(SectorEditor)

    def _connect(self):
        editor = self._dependency.get(ProblemsEditor)
        editor.problemsChanged.connect(self._on_problems_changed)
        editor.problemAdded.connect(self._on_problems_changed)
        editor.problemRemoved.connect(self._on_problems_changed)
        self.model.cellsChanged.connect(self.view.update_UI)

    def _on_problems_changed(self, arg:bool):
        editor    = self._dependency.get(ProblemsEditor)
        self.model.problems_changed(editor.problems)

