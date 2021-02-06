from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from models.dicts import SectorDict
from models.cell_data import SectorCellDataBuilder
from APImodels.sector import Sector

class SectorScrollAreaModel(QObject):

    cellModelsChanged = pyqtSignal(bool)
    cell_data = {} 

    def __init__(self, sector_setting: SectorDict):
        super().__init__()
        self.sector_setting = sector_setting
        self.builder = SectorCellDataBuilder()
        self.n_col   = self.sector_setting.length()
        self._sectors = []

    @property
    def sectors(self):
        return self._sectors

    @sectors.setter
    def sectors(self, value):
        self._sectors    = value
        self.cell_data = self.__generate_cell_data_dictionary()
        self.cellModelsChanged.emit(True)
    
    def get_default_sector_cell_data(self, col:int):
        return self.builder.build_from_col(col)

    def __generate_cell_data_dictionary(self):
        # generate a dictionary containing column as keys, and sector cell data
        # as values
        data =  [self.__data(sector) for sector in self.sectors]
        return dict({d.col: d for d in data})

    def __data(self, sector: Sector):
        return self.builder.build_from_sector(sector)