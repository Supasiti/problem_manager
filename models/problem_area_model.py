from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import NamedTuple

from services.setting import Setting
from services.grade_setting import GradeSetting
from services.sector_setting import SectorSetting
from services.colour_setting import ColourSetting
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
    
class ProblemAreaDataBuilder(QObject):

    def __init__(self):
        super().__init__()
        self._grade_setting  = Setting.get(GradeSetting)
        self._sector_setting = Setting.get(SectorSetting)
        self._builder        = ProblemCellDataBuilder()
        
        self._n_row = self._grade_setting.length()
        self._n_col = self._sector_setting.length()

    @property 
    def n_cell(self):
        return self._n_row * self._n_col
    
    def _cell_coord(self, index:int):
        return (index // self._n_col, index % self._n_col)

    def no_problems(self):
        cells = [self._builder.empty_cell(*self._cell_coord(index))
                for index in range(self.n_cell)]
        return ProblemAreaData(tuple(cells))

    def from_problems(self, problems:tuple[Problem,...], non_empty_cells:tuple ):
        # Arguments:
        #   problems        : a tuple of type Problem
        #   non_empty_cells : a tuple of type (row, col) - indicate that these are non empty
        new_cell_data  = [self._cell_data(p) for p in problems]
        new_cell_coord = [(d.row, d.col) for d in new_cell_data]
        empty_cells    = [self._builder.empty_cell(*_tuple) 
                            for _tuple in non_empty_cells
                            if not _tuple in new_cell_coord]
        new_cell_data += empty_cells
        return ProblemAreaData(tuple(new_cell_data))

    def _cell_data(self, problem:Problem):
        return self._builder.from_problem(problem)

    def from_problem(self, problem:Problem):
        assert(type(problem) == Problem)
        cell_data = self._cell_data(problem)
        return ProblemAreaData((cell_data,))
    
    def empty_cell(self, problem :Problem):
        assert(type(problem) == Problem)
        _row      = self._grade_setting.get_row(problem.grade)
        _col      = self._sector_setting.get_col(problem.sector)
        cell_data = self._builder.empty_cell(_row, _col) 
        return ProblemAreaData((cell_data,))
    

class ProblemAreaModel(QObject):

    cellsChanged = pyqtSignal(bool)
    _changes     : ProblemAreaData

    def __init__(self, side_panels:ProblemAreaPanelData):
        super().__init__()
        self._builder = ProblemAreaDataBuilder()
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
        new_cells = [(d.row, d.col) for d in new_data]
        old_data_to_retain = [ d for d in old_data if not (d.row, d.col) in new_cells]
        new_data += old_data_to_retain
        self.data = ProblemAreaData(tuple(new_data))

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

        non_empty_cells = [(c.row, c.col) for c in self.data.cells if c.id != 0]
        self.changes = self._builder.from_problems(problems, tuple(non_empty_cells))

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
        setting = Setting.get(ColourSetting)
        bg_colour = setting.get_bg_colour('default')
        text_colour = setting.get_text_colour('default')
        return InfoCellData(bg_colour, text_colour)

# class InfoCellModel(self):

#     cellsChanged = pyqtSignal(bool)