# Main presenter
#
# contains all the informations being presented on MainView
from typing import NamedTuple
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class MainViewStaticData(NamedTuple):
    # contains all the static data required by Main View

    title : str
    width : int
    height : int

    @staticmethod
    def default():
        return MainViewStaticData('Problem Manager', 1200, 800)

class MainViewDynamicData(NamedTuple):
    # contains all the dynamic data required by Main View
    # especially references to all 4 stations

    top_station : QWidget
    work_station : QWidget
    bottom_station : QWidget
    tool_station : QWidget

    @staticmethod
    def default():
        return MainViewDynamicData(None, None, None, None)

class MainModel(QObject):
    # store all the information on the view
    
    dataChanged = pyqtSignal(bool) 

    def __init__(self, 
        static_data  : MainViewStaticData = MainViewStaticData.default(),
        dynamic_data : MainViewDynamicData = MainViewDynamicData.default()
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
    def dynamic_data(self, data: MainViewDynamicData):
        self._dynamic_data = data
        self.dataChanged.emit(True)

      