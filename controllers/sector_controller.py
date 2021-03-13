
from services.problems_editor import ProblemsEditor
from services.dependency_service import DependencyService
from services.sector_editor import SectorEditor
from models.sector_area_model import SectorAreaModel
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    _dependency : DependencyService
    _sector_selected :str = None
    _next_sector_id  = 0

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
        self._sector_editor.sectorsChanged.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        editor    = self._dependency.get(ProblemsEditor)
        self.model.problems_changed(editor.problems)

    def select_sector(self, col:int) -> None:
        self._sector_selected = self._sector_editor.get_sector(col)


    def rename_sector(self, change_to:str) -> None:
        if not self._sector_selected is None:
            if not change_to.lower() in self._sector_editor.get_all_sectors():
                self._sector_editor.change_name(self._sector_selected, change_to.lower())
                self._sector_selected = None


    def insert_sector_to_the_left(self) -> None:
        col = self._sector_editor.get_col(self._sector_selected)
        self._sector_editor.add_sector('unname_'+ str(self._next_sector_id), col)
        self._next_sector_id += 1

    def insert_sector_to_the_right(self) -> None:
        if not self._sector_selected is None:
            col = self._sector_editor.get_col(self._sector_selected)
            self._sector_editor.add_sector('unname_'+ str(self._next_sector_id), col+1)
            self._next_sector_id += 1
            self._sector_selected = None
    
    def delete_sector(self) -> None:
        if not self._sector_selected is None:
            self._sector_editor.remove_sector(self._sector_selected)
            self._sector_selected = None