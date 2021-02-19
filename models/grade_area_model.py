from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import NamedTuple

from services.grade_setting import GradeSetting
from services.colour_setting import ColourSetting
from models.cell_data import GradeCellData, GradeCellDataBuilder, GradeCountData, GradeCountDataBuilder
from APImodels.problem import Problem
from APImodels.grade import Grade

class GradeAreaData(NamedTuple):
    width : int
    cells : tuple[GradeCellData,...]

class GradeAreaDataBuilder():

    def __init__(self, grade_setting: GradeSetting):
        super().__init__()
        self.grade_setting  = grade_setting
        self.builder = GradeCellDataBuilder(self.grade_setting)
        self.n_row   = self.grade_setting.length()

    def default(self):
        cells = [self.builder.build(row) for row in range(self.n_row)]
        cells.sort(key= lambda x : x.row)
        return GradeAreaData(160, tuple(cells))


class GradeCountsData(NamedTuple):
    cells : tuple[GradeCountData,...]

    def get_cell(self, row:int):
        cell = [cell for cell in self.cells if cell.row == row]
        return cell[0] if len(cell) > 0 else None


class GradeCountsDataBuilder():

    def __init__(self, grade_setting: GradeSetting, colour_setting:ColourSetting):
        super().__init__()
        self._grade_setting  = grade_setting
        self._colour_setting = colour_setting
        self._builder = GradeCountDataBuilder(self._grade_setting, self._colour_setting )

        self.n_row   = self._grade_setting.length()
        self._grades = self._grade_setting.get_all_grades()

    def default(self):
        cells = [self._builder.build(row, 0) for row in range(self.n_row)] 
        cells.sort(key= lambda x : x.row)
        return GradeCountsData(tuple(cells))

    def from_problems(self, problems:tuple[Problem,...]):
        prob = tuple(problems)
        if len(prob) == 0 :
            return self.default()
        cell_data = [(self._grade_setting.get_row(g), self._counts(g, prob) ) for g in self._grades]
        cells     = [self._builder.build(d[0], d[1]) for d in cell_data]
        cells.sort(key= lambda x : x.row)
        return GradeCountsData(tuple(cells))

    def _counts(self, grade:Grade, problems:tuple[Problem,...]):
        return len([p for p in problems if p.grade == grade])

class GradeAreaModel(QObject):
    
    countsChanged = pyqtSignal(bool)
    
    def __init__(self, data : GradeAreaData, counts : GradeCountsData):
        super().__init__()
        self.static  = data
        self._counts = counts

    @property
    def counts(self):
        return self._counts

    @counts.setter
    def counts(self, value: GradeCountsData):
        self._counts = value
        self.countsChanged.emit(True)
