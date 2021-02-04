#  Model for the bottom station

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class BottomStationModel(QObject):

    contentPathChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._content_path = r'/Users/thara/Desktop/Programming/python/problem_manager/Contents'


    @property
    def content_path(self):
        return self._content_path

    @content_path.setter
    def content_path(self, value:str):
    
        self._content_path = value
        self.contentPathChanged.emit(value)