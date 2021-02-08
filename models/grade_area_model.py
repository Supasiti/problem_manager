from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import Tuple, NamedTuple

from models.dicts import GradeDict, ColourDict
from models.cell_data import GradeCellData, GradeCellDataBuilder, GradeCountData, GradeCountDataBuilder

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
        self.grade_setting  = grade_setting
        self.colour_setting = colour_setting
        self.builder = GradeCountDataBuilder(self.grade_setting, self.colour_setting )

        self.n_row   = self.grade_setting.length()

    def default(self):
        cells = [self.builder.build(row, 0) for row in range(self.n_row)] ## need to change
        cells.sort(key= lambda x : x.row)
        return GradeCountsData(tuple(cells))


class GradeAreaModel(QObject):
    
    countsChanged = pyqtSignal(bool)
    _changes : GradeCountsData

    def __init__(self, data : GradeAreaData, counts : GradeCountsData):
        super().__init__()
        self.static  = data
        self._counts = counts
        self.changes = counts

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value: GradeCountsData):
        # self.__update_data(value)
        self._changes = value
        self.countsChanged.emit(True)


    # def __update_data(self, value: SectorAreaData):
    #     old_data  = list(self._data.cells)
    #     new_data  = list(value.cells)
    #     new_cells = [d.col for d in new_data]
    #     old_data_to_retain = [ d for d in old_data if not d.col in new_cells]
    #     new_data += old_data_to_retain
    #     self._data = SectorAreaData(48, tuple(new_data))