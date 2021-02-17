# Tool station model
# 
# contains all the informations being presented in ToolStation
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from views.editor_view import EditorView

class ToolData(NamedTuple):

    width      : int
    editor     : EditorView

    @staticmethod
    def default():
        return ToolData(280, None)

class ToolStationModel(QObject):
    
    dataChanged = pyqtSignal(bool) 

    def __init__(self, view_data : ToolData = ToolData.default()):
        super().__init__()
        self._data  = view_data

    @property
    def view_data(self):
        return self._data
    
    @view_data.setter
    def view_data(self, data: str):
        self._data = data
        self.dataChanged.emit(True)