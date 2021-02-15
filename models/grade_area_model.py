from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import Tuple, NamedTuple

from models.dicts import GradeDict, ColourDict
from models.cell_data import GradeCellData, GradeCellDataBuilder, GradeCountData, GradeCountDataBuilder
from APImodels.problem import Problem

class GradeAreaData(NamedTuple):
    width : int
    cells : Tuple[GradeCellData,...]

class GradeAreaDataBuilder():

    def __init__(self, grade_setting: GradeDict, colour_setting:ColourDict):
        super().__init__()
        self.grade_setting  = grade_setting
        self.colour_setting = colour_setting
        self.builder = GradeCellDataBuilder(self.grade_setting, self.colour_setting)
       
        self.n_row   = self.grade_setting.length()

    def default(self):
        cells = [self.builder.build(row) for row in range(self.n_row)]
        cells.sort(key= lambda x : x.row)
        return GradeAreaData(154, tuple(cells))


class GradeCountsData(NamedTuple):
    cells : Tuple[GradeCountData,...]

class GradeCountsDataBuilder():

    def __init__(self, grade_setting: GradeDict, colour_setting:ColourDict):
        super().__init__()
        self._grade_setting  = grade_setting
        self._colour_setting = colour_setting
        self._builder = GradeCountDataBuilder(self._grade_setting, self._colour_setting )

        self.n_row   = self._grade_setting.length()
        self._grades = self._grade_setting.get_all_grades()

    def default(self):
        cells = [self._builder.build(row, 0) for row in range(self.n_row)] ## need to change
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

    def _counts(self, grade:str, problems:tuple[Problem,...]):
        return len([p for p in problems if str(p.grade) == grade])

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
