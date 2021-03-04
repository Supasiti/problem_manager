#  Model for the work station
from typing import NamedTuple
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from services.colour_setting import ColourSetting
from services.setting import Setting
from APImodels.colour import Colour

class WorkStaticData(NamedTuple):

    bg_colour    : Colour 
    
    @staticmethod
    def default():
        colour = Setting.get(ColourSetting).get_bg_colour('default_light')
        return WorkStaticData(colour)

class WorkDynamicData(NamedTuple):
    main_view  : QWidget

    @staticmethod
    def default():
        return WorkDynamicData(None)

class WorkStationModel(QObject):

    dataChanged = pyqtSignal(bool)

    def __init__(self, dynamic_data : WorkDynamicData ):
        super().__init__()
        self._static_data  = WorkStaticData.default()
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
        self.dataChanged.emit(value)