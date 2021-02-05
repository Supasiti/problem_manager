from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from models.dicts import SectorDict
from models.cell_model import SectorCellModelBuilder
from APImodels.sector import Sector

class SectorScrollAreaModel(QObject):

    cellModelsChanged = pyqtSignal(bool)
    cell_models = {} 

    def __init__(self, sector_setting: SectorDict):
        super().__init__()
        self.sector_setting = sector_setting
        self.builder = SectorCellModelBuilder()
        self.n_col   = self.sector_setting.length()
        self._sectors = []

    @property
    def sectors(self):
        return self._sectors

    @sectors.setter
    def sectors(self, value):
        self._sectors    = value
        self.cell_models = self.__generate_cell_model_dictionary()
        self.cellModelsChanged.emit(True)
    
    def get_default_sector_cell_model(self, col:int):
        return self.builder.build_from_col(col)

    def __generate_cell_model_dictionary(self):
        # generate a dictionary containing (column) as keys, and sector cell models
        # as values
        models =  [self.__model(sector) for sector in self.sectors]
        return dict({model.col: model for model in models})

    def __model(self, sector: Sector):
        return self.builder.build_from_sector(sector)