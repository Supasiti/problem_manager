# Tool station model
# 
# contains all the informations being presented in ToolStation
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class ToolStaticData(NamedTuple):

    width      : int
    
    @staticmethod
    def default():
        return ToolStaticData(280)

class ToolStationModel(QObject):
    
    dataChanged = pyqtSignal(bool) 

    def __init__(self, 
        static_data  : ToolStaticData = ToolStaticData.default(),
        dynamic_data : int = None 
        ):

        super().__init__()
        self._static_data  = static_data
        self._dynamic_data = dynamic_data
    
    @property
    def static_data(self):
        return self._static_data

    @property
    def dynamic_data(self):
        return self._date_str
    
    @dynamic_data.setter
    def dynamic_data(self, data: str):
        self._dynamic_data = data
        self.dataChanged.emit(True)