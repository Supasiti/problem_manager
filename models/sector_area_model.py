from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import Tuple, NamedTuple

from models.dicts import SectorDict, ColourDict
from models.cell_data import SectorCellData, SectorCellDataBuilder
from APImodels.sector import Sector

class SectorAreaData(NamedTuple):
    height : int
    cells : Tuple[SectorCellData,...]

class SectorAreaDataBuilder():
   
    def __init__(self, sector_setting: SectorDict, colour_setting:ColourDict):
        super().__init__()
        self.sector_setting = sector_setting
        self.colour_setting = colour_setting
        self.builder = SectorCellDataBuilder(self.sector_setting, self.colour_setting)

        self.n_col   = self.sector_setting.length()

    def default(self):
        cells = [self.builder.build_from_col(index) for index in range(self.n_col)]
        cells.sort(key= lambda x : x.col)
        return SectorAreaData(48, tuple(cells))

    def build_from_sectors(self, sectors:Tuple[Sector,...]):
        cells = [self.builder.build_from_sector(s) for s in sectors]
        cells.sort(key= lambda x : x.col)
        return SectorAreaData(48, tuple(cells))

    
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