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
        self._sectors = []

    def default(self):
        n_col   = self.sector_setting.length()
        cells = [self.builder.build_from_col(index) for index in range(n_col)]
        cells.sort(key= lambda x : x.col)
        print(len(cells))
        return SectorAreaData(48, tuple(cells))

    # @property
    # def sectors(self):
    #     return self._sectors

    # @sectors.setter
    # def sectors(self, value):
    #     self._sectors    = value
    #     self.cell_data = self.__generate_cell_data_dictionary()
    #     self.cellModelsChanged.emit(True)
    
    # def get_default_sector_cell_data(self, col:int):
    #     return self.builder.build_from_col(col)

    # def __generate_cell_data_dictionary(self):
    #     # generate a dictionary containing column as keys, and sector cell data
    #     # as values
    #     data =  [self.__data(sector) for sector in self.sectors]
    #     return dict({d.col: d for d in data})

    # def __data(self, sector: Sector):
    #     return self.builder.build_from_sector(sector)

    
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
        pass