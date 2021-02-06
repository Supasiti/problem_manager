#  Model for the bottom station
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class BottomStaticData(NamedTuple):

    height       : int
    label_text   : str
    label_width  : int
    button_text  : str
    button_width : int
    label_width  : int
    
    @staticmethod
    def default():
        return BottomStaticData(80, 'Content Path:',100, 'Change', 100)


class BottomStationModel(QObject):

    contentPathChanged = pyqtSignal(str)

    def __init__(self,
        static_data  : BottomStaticData = BottomStaticData.default(),
        dynamic_data : str = r'/Users/thara/Desktop/Programming/python/problem_manager/Contents'
        ):
        super().__init__()
        self._static_data  = static_data
        self._dynamic_data = dynamic_data

    @property
    def static_data(self):
        return self._static_data

    @property
    def dynamic_data(self):
        return self._dynamic_data

    @dynamic_data.setter
    def dynamic_data(self, value:str):
        self._dynamic_data = value
        self.contentPathChanged.emit(value)