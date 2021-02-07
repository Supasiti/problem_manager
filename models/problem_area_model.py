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
    
    def __cell_coord(self, index:int):
        return (index // self.n_col, index % self.n_col)

    def no_problems(self):
        cells = [self.builder.empty_cell(index // self.n_col, index % self.n_col) for index in range(self.n_cell)]
        return ProblemAreaData(tuple(cells))

    def build_from_problems(self, problems:Tuple[Problem,...]):
        data = list(problems)
        new_cell_data  = [self.__cell_data(p) for p in data]
        new_cell_coord = [(d.row, d.col) for d in new_cell_data]
        empty_cells    = [self.builder.empty_cell(*self.__cell_coord(index)) 
                            for index in range(self.n_cell) 
                            if not self.__cell_coord(index) in new_cell_coord]
        new_cell_data += empty_cells
        return ProblemAreaData(tuple(new_cell_data))

    def __cell_data(self, problem:Problem):
        return self.builder.build_from_problem(problem)

    # def add_problems(self, problems:Tuple[Problem,...]):
    #     # can't just add problems
    #     # need to replace old problems with the same id with new ones
    #     new_prob = list(problems)
    #     if len(new_prob) == 0:
    #         raise ValueError('add_problem() do not accept empty tuple.')
    #     if len(self.problems) != 0:
    #         old_prob = list(self.problems)
    #         new_ids  = {p.id for p in new_prob}
    #         old_prob = [p for p in old_prob if not p.id in new_ids]
    #         new_prob += old_prob
    #     self.problems = tuple(new_prob)
    

class ProblemAreaModel(QObject):

    cellsChanged = pyqtSignal(bool)
    _changes : ProblemAreaData

    def __init__(self, data : ProblemAreaData):
        super().__init__()
        self._data   = data
        self.changes = data

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value: ProblemAreaData):
        self.__update_data(value)
        self._changes = value
        self.cellsChanged.emit(True)


    def __update_data(self, value: ProblemAreaData):
        old_data  = list(self._data.cells)
        new_data  = list(value.cells)
        new_cells = [(d.row, d.col) for d in new_data]
        old_data_to_retain = [ d for d in old_data if not (d.row, d.col) in new_cells]
        new_data += old_data_to_retain
        self._data = ProblemAreaData(tuple(new_data))
        