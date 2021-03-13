from __future__ import annotations
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import NamedTuple

from services.setting import Setting
from services.grade_setting import GradeSetting
from services.colour_setting import ColourSetting
from services.sector_editor import SectorEditor
from models.problem_cell_data import ProblemCellDataBuilder, ProblemCellData
from APImodels.problem import Problem
from APImodels.colour import Colour

class ProblemAreaPanelData(NamedTuple):
    info_view   : QWidget
    sector_view : QWidget
    grade_view  : QWidget
    top_margin  : int = 52 
    left_margin : int = 164

class ProblemAreaData(NamedTuple):
    cells : tuple[ProblemCellData,...] 
    n_row : int
    n_col : int
    
class ProblemAreaDataBuilder(QObject):

    def __init__(self, sector_editor:SectorEditor):
        super().__init__()
        self._grade_setting  = Setting.get(GradeSetting)
        self._sector_setting = sector_editor
        self._builder        = ProblemCellDataBuilder(sector_editor)

    @property
    def n_row(self) ->int :
        return self._grade_setting.length()

    @property
    def n_col(self) ->int :
        return self._sector_setting.length() 

    @property 
    def n_cell(self) -> int:
        return self.n_row * self.n_col
    
    def _cell_coord(self, index:int):
        return (index // self.n_col, index % self.n_col)

    def no_problems(self):
        cells = [self._builder.empty_cell(*self._cell_coord(index))
                for index in range(self.n_cell)]
        return ProblemAreaData(tuple(cells), self.n_row, self.n_col)
    
    def from_problems(self, problems:tuple[Problem,...], previous_data:ProblemAreaData) -> ProblemAreaData:
        # Arguments:
        #   problems      : a tuple of type Problem
        #   previous_data : ProblemAreaData 
        new_cell_data   = [self._cell_data(p) for p in problems]
        new_cell_coord  = [(d.row, d.col) for d in new_cell_data]
        cell_to_update  = self._cell_to_update_coord(problems, previous_data)
        new_empty_cells = [ self._builder.empty_cell(*_tuple) 
                            for _tuple in cell_to_update
                            if not _tuple in new_cell_coord]
        new_cell_data  += new_empty_cells
        return ProblemAreaData(tuple(new_cell_data), self.n_row, self.n_col) 

    def _cell_to_update_coord(self, problems:tuple[Problem,...], previous_data:ProblemAreaData) -> list:
        # return a list of tuple (row, col) of coordinates of cells to be updated
        cell_to_update = [(c.row, c.col) for c in previous_data.cells if c.id != 0]
        if previous_data.n_row < self.n_row:
            # add bottom rows
            max_col     = min(previous_data.n_col, self.n_col)
            bottom_rows = [(row,col) for row in range(self.n_row)[previous_data.n_row:] for col in range(max_col)]
            cell_to_update += bottom_rows

        if previous_data.n_col < self.n_col:
            # add right hand columns
            max_row    = max(previous_data.n_row, self.n_row)
            right_cols = [(row,col) for row in range(max_row) for col in range(self.n_col)[previous_data.n_col:]]
            cell_to_update += right_cols
        return cell_to_update
            
    def _cell_data(self, problem:Problem):
        return self._builder.from_problem(problem)

    def from_problem(self, problem:Problem):
        # assume that no column or row being added/removed
        assert(type(problem) == Problem)
        cell_data = self._cell_data(problem)
        return ProblemAreaData((cell_data,), self.n_row, self.n_col)
    
    def empty_cell(self, problem :Problem):
        # assume that no column or row being added/removed
        assert(type(problem) == Problem)
        _row      = self._grade_setting.get_row(problem.grade)
        _col      = self._sector_setting.get_col(problem.sector)
        cell_data = self._builder.empty_cell(_row, _col) 
        return ProblemAreaData((cell_data,), self.n_row, self.n_col)
    

class ProblemAreaModel(QObject):

    cellsChanged = pyqtSignal(bool)
    _changes     : ProblemAreaData

    def __init__(self, side_panels:ProblemAreaPanelData, sector_editor:SectorEditor):
        super().__init__()
        self._builder = ProblemAreaDataBuilder(sector_editor)
        self.data    = self._builder.no_problems()
        self.changes = self._builder.no_problems() 
        self.panels  = side_panels

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value: ProblemAreaData) -> None:
        self._update_data(value)
        self._changes = value
        self.cellsChanged.emit(True)

    def _update_data(self, value: ProblemAreaData) -> None:
        old_data  = list(self.data.cells)
        new_data  = list(value.cells)
        new_cells = ((d.row, d.col) for d in new_data)
        old_data_to_retain = [ d for d in old_data if not (d.row, d.col) in new_cells]
        new_data += old_data_to_retain
        self.data = ProblemAreaData(tuple(new_data), value.n_row, value.n_col) 

    def add_problem(self, problem: Problem) -> None:
        # Call when the editor notifies that a problem is added to that cell. 
        # We only need to change that cell. 
        assert(type(problem) == Problem)
        self.changes = self._builder.from_problem(problem)

    def update_problems(self, problems:tuple[Problem,...]) -> None:
        # call when the editor notifies that a new set of problems is available and this 
        # set contains all the problems to be shown on screen.
        # To optimise algo, all non-empty cell will be converted either to new data or
        # empty cell. We are expecting about 60 problems on screens at any one time, so
        # at most we only need to convert 120 cells, instead of 247 cells
        self.changes = self._builder.from_problems(problems, self.data)

    def remove_problem(self, problem: Problem) -> None:
        # Call when the editor notifies that a problem is removed from that cell. 
        # We only need to change that cell. 
        assert(type(problem) == Problem)
        self.changes = self._builder.empty_cell(problem)


class InfoCellData(NamedTuple):

    bg_colour   : Colour
    text_colour : Colour 
    width  : int = 160
    height : int = 48
    inner_width  : int = 52
    inner_height : int = 23

    @staticmethod
    def default() -> InfoCellData:
        setting   = Setting.get(ColourSetting)
        bg_colour = setting.get_bg_colour('default')
        text_colour = setting.get_text_colour('default')
        return InfoCellData(bg_colour, text_colour)

class InfoCellModel(QObject):

    countsChanged = pyqtSignal(int)
    aimChanged    = pyqtSignal(int)

    _aim    : int
    _counts : int

    def __init__(self):
        super().__init__()
        self.static_data = InfoCellData.default()
        self.aim    = Setting.get(GradeSetting).get_total_aim()
        self.counts = 0

    @property
    def aim(self) -> int:
        return self._aim
    
    @aim.setter
    def aim(self, value:int) -> None:
        self._aim = value
        self.aimChanged.emit(value)

    @property 
    def counts(self) -> None:
        return self._counts

    @counts.setter
    def counts(self, value:int) -> None:
        self._counts = value
        self.countsChanged.emit(value)

        
