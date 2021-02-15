from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import Tuple, NamedTuple

from models.dicts import GradeDict, SectorDict, ColourDict
from models.problem_cell_data import ProblemCellDataBuilder, ProblemCellData
from APImodels.problem import Problem

class ProblemAreaData(NamedTuple):
    cells : Tuple[ProblemCellData,...]

class ProblemAreaDataBuilder(QObject):

    def __init__(self, 
        grade_setting : GradeDict, 
        colour_setting: ColourDict, 
        sector_setting: SectorDict):
        super().__init__()
        self.grade_setting  = grade_setting
        self.colour_setting = colour_setting
        self.sector_setting = sector_setting
        self.builder = ProblemCellDataBuilder(
                        self.grade_setting, self.colour_setting, self.sector_setting)
        
        self.n_row = self.grade_setting.length()
        self.n_col = self.sector_setting.length()

    @property 
    def n_cell(self):
        return self.n_row * self.n_col
    
    def _cell_coord(self, index:int):
        return (index // self.n_col, index % self.n_col)

    def no_problems(self):
        cells = [self.builder.empty_cell(*self._cell_coord(index))
                for index in range(self.n_cell)]
        return ProblemAreaData(tuple(cells))

    def from_problems(self, problems:Tuple[Problem,...]):

        new_cell_data  = [self._cell_data(p) for p in problems]
        new_cell_coord = [(d.row, d.col) for d in new_cell_data]
        empty_cells    = [self.builder.empty_cell(*self._cell_coord(index)) 
                            for index in range(self.n_cell) 
                            if not self._cell_coord(index) in new_cell_coord]
        new_cell_data += empty_cells
        return ProblemAreaData(tuple(new_cell_data))

    def _cell_data(self, problem:Problem):
        return self.builder.from_problem(problem)

    def from_problem(self, problem:Problem):
        assert(type(problem) == Problem)
        cell_data = self._cell_data(problem)
        return ProblemAreaData((cell_data,))
    
    def empty_cell(self, problem :Problem):
        assert(type(problem) == Problem)
        _row = self.grade_setting.get_row(str(problem.grade))
        _col = self.sector_setting.get_col(problem.sector)
        cell_data = self.builder.empty_cell(_row, _col) 
        return ProblemAreaData((cell_data,))
    
class ProblemAreaModel(QObject):

    cellsChanged       = pyqtSignal(bool)
    sectorCellsChanged = pyqtSignal(dict)
    gradeCellsChanged  = pyqtSignal(dict)

    _changes     : ProblemAreaData
    sector_count : dict[int: int]
    grade_count  : dict[int: int]

    def __init__(self, data : ProblemAreaData):
        super().__init__()
        self.data     = data
        self.n_row    = max([d.row for d in self.data.cells ])+ 1
        self.n_col    = max([d.col for d in self.data.cells ])+ 1
        self.changes  = data

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value: ProblemAreaData):
        self._update_data(value)
        self._changes = value
        self.cellsChanged.emit(True)

    def _update_data(self, value: ProblemAreaData):
        old_data  = list(self.data.cells)
        new_data  = list(value.cells)
        new_cells = [(d.row, d.col) for d in new_data]
        old_data_to_retain = [ d for d in old_data if not (d.row, d.col) in new_cells]
        new_data += old_data_to_retain
        self.data = ProblemAreaData(tuple(new_data))
