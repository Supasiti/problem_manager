from __future__ import annotations
from typing import NamedTuple
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class ToolData(NamedTuple):

    tools     : tuple[QWidget,...]
    width     : int = 280

    @staticmethod
    def default() -> ToolData:
        return ToolData((QWidget(),))


class ToolStationModel(QObject):
    # Tool station model
    # 
    # contains all the informations being presented in ToolStation
    dataChanged = pyqtSignal(bool) 

    def __init__(self):
        super().__init__()
        self._data  = ToolData.default()

    @property
    def view_data(self):
        return self._data
    
    @view_data.setter
    def view_data(self, data: str):
        self._data = data
        self.dataChanged.emit(True)

    def set_widgets(self, widgets:tuple[QWidget,...]) -> None:
        self.view_data = ToolData(widgets)