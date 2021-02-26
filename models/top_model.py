# Top station model
# 
# contains all the informations being presented in TopStation
from typing import NamedTuple
from datetime import date
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class TopStaticData(NamedTuple):

    height      : int
    width       : int
    label_text  : str
    label_width : int
    
    
    @staticmethod
    def default():
        return TopStaticData(40, 280, 'Date', 60)

class TopStationModel(QObject):
    
    dataChanged = pyqtSignal(str) 

    def __init__(self, 
        static_data  : TopStaticData = TopStaticData.default(),
        _date        : str = date.today().isoformat()
        ):

        super().__init__()
        self._static_data  = static_data
        self._date_str     = _date
    
    @property
    def static_data(self):
        return self._static_data

    @property
    def date_str(self):
        return self._date_str
    
    @date_str.setter
    def date_str(self, data: str):
        self._date_str = data
        self.dataChanged.emit(data)