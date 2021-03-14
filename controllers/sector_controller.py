from __future__ import annotations
from abc import ABC, abstractmethod

from services.problems_editor import ProblemsEditor
from services.dependency_service import DependencyService
from services.sector_editor import SectorEditor
from models.sector_area_model import SectorAreaModel
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    _dependency : DependencyService
    _state : State
    sector_selected :str = None
    next_sector_id :int = 0

    def __init__(self, dependency : DependencyService):
        self._setup_dependencies(dependency)
        self.change_to_state(EditingState())

        self.model    = SectorAreaModel(self.sector_editor) # load model
        self.view     = SectorArea(self, self.model)         # load view
        self._connect()
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self.sector_editor = self._dependency.get(SectorEditor)

    def change_to_state(self, state:State) -> None:
        self._state = state
        self._state.context = self

    def _connect(self):
        editor = self._dependency.get(ProblemsEditor)
        editor.problemsChanged.connect(self._on_problems_changed)
        editor.problemAdded.connect(self._on_problems_changed)
        editor.problemRemoved.connect(self._on_problems_changed)
        editor.stateChanged.connect(self._on_state_changed)
        self.model.cellsChanged.connect(self.view.update_UI)
        self.sector_editor.sectorsChanged.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        editor    = self._dependency.get(ProblemsEditor)
        self.model.problems_changed(editor.problems)

    def _on_state_changed(self, state_name:str) -> None:
        if state_name == 'editing':
            self.change_to_state(EditingState())
            self.view.set_popup_menu_visibility(True)
        elif state_name == 'viewing':
            self.change_to_state(ViewingState())
            self.view.set_popup_menu_visibility(False)
        else:
            raise ValueError('Main Controller: incorrect state name')

    def select_sector(self, col:int) -> None:
        self.sector_selected = self.sector_editor.get_sector(col)

    def rename_sector(self, change_to:str) -> None:
        self._state.rename_sector(change_to)

    def insert_sector_to_the_left(self) -> None:
        self._state.insert_sector_to_the_left()

    def insert_sector_to_the_right(self) -> None:
        self._state.insert_sector_to_the_right()
    
    def delete_sector(self) -> None:
        self._state.delete_sector()
     

class State(ABC):

    _context     : SectorAreaController

    @property
    def context(self) -> SectorAreaController:
        return self._context

    @context.setter
    def context(self, context: SectorAreaController) -> None:
        self._context = context
    
    @abstractmethod
    def rename_sector(self, change_to:str) -> None:
        pass

    @abstractmethod
    def insert_sector_to_the_left(self) -> None:
        pass

    @abstractmethod
    def insert_sector_to_the_right(self) -> None:
        pass

    @abstractmethod
    def delete_sector(self) -> None:
        pass

class EditingState(State):

    def rename_sector(self, change_to:str) -> None:
        if self.context.sector_selected is None:
            return
        if not change_to.lower() in self.context.sector_editor.get_all_sectors():
            self.context.sector_editor.change_name(self.context.sector_selected, change_to.lower())
            self.context.sector_selected = None

    def insert_sector_to_the_left(self) -> None:
        if self.context.sector_selected is None:
            return
        col = self.context.sector_editor.get_col(self.context.sector_selected)
        self.context.sector_editor.add_sector('unname_'+ str(self.context.next_sector_id), col)
        self.context.next_sector_id += 1

    def insert_sector_to_the_right(self) -> None:
        if self.context.sector_selected is None:
            return
        col = self.context.sector_editor.get_col(self.context.sector_selected)
        self.context.sector_editor.add_sector('unname_'+ str(self.context.next_sector_id), col+1)
        self.context.next_sector_id += 1
        self.context.sector_selected = None
    
    def delete_sector(self) -> None:
        if self.context.sector_selected is None:
            return
        self.context.sector_editor.remove_sector(self.context.sector_selected)
        self.context.sector_selected = None

class ViewingState(State):

    def rename_sector(self, change_to:str) -> None:
        pass

    def insert_sector_to_the_left(self) -> None:
        pass

    def insert_sector_to_the_right(self) -> None:
        pass
    
    def delete_sector(self) -> None:
        pass