from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import Tuple, NamedTuple

from services.colour_setting import ColourSetting
from models.dicts import SectorDict
from models.cell_data import SectorCellData, SectorCellDataBuilder
from APImodels.sector import Sector
from APImodels.problem import Problem

class SectorAreaData(NamedTuple):
    height : int
    cells : Tuple[SectorCellData,...]

class SectorAreaDataBuilder():
   
    def __init__(self, sector_setting: SectorDict, colour_setting:ColourSetting):
        super().__init__()
        self._sector_setting = sector_setting
        self._colour_setting = colour_setting
        self._builder        = SectorCellDataBuilder(self._sector_setting, self._colour_setting)

        self.n_col           = self._sector_setting.length()
        self._sectors        = self._sector_setting.get_all_sectors()

    def default(self):
        cells = [self._builder.from_col(index) for index in range(self.n_col)]
        cells.sort(key= lambda x : x.col)
        return SectorAreaData(48, tuple(cells))

    def from_problems(self, problems:tuple[Problem,...]):
        prob = tuple(problems)
        if len(prob) == 0 :
            return self.default()
        set_date = self._last_setting_date(prob)
        sectors  = [Sector.from_problems(s, prob, set_date) for s in self._sectors]
        cells    = list([self._builder.from_sector(s) for s in sectors ])
        cells.sort(key= lambda x : x.col)
        return SectorAreaData(48, tuple(cells))

    def _last_setting_date(self, problems:tuple[Problem,...]):
        prob = tuple(problems)
        if len(prob) == 0: 
            raise ValueError('_get_last_setting_date() don\'t accept empty generator')
        return max([p.set_date for p in prob]) 

class SectorAreaModel(QObject):
    
    cellsChanged = pyqtSignal(bool)
    _changes : SectorAreaData

    def __init__(self, data : SectorAreaData):
        super().__init__()
        self._data   = data
        self.changes = data

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value: SectorAreaData):
        self.__update_data(value)
        self._changes = value
        self.cellsChanged.emit(True)


    def __update_data(self, value: SectorAreaData):
        old_data  = list(self._data.cells)
        new_data  = list(value.cells)
        new_cells = [d.col for d in new_data]
        old_data_to_retain = [ d for d in old_data if not d.col in new_cells]
        new_data += old_data_to_retain
        self._data = SectorAreaData(48, tuple(new_data))