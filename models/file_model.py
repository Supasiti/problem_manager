# file viewer  model
# 
# contains all the informations being presented in file viewer
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class FileStaticData(NamedTuple):

    width      : int
   
    @staticmethod
    def default():
        return FileStaticData(276)


class FileData(NamedTuple):

    filenames : tuple[str]


class FileViewModel(QObject):
    
    dataChanged = pyqtSignal(bool) 

    def __init__(self, 
        static_data  : FileStaticData = FileStaticData.default(),
        data         : FileData = FileData(tuple())
        ):

        super().__init__()
        self._static_data  = static_data
        self._data = data
    
    @property
    def static_data(self):
        return self._static_data

    @property
    def view_data(self):
        return self._data
    
    @view_data.setter
    def view_data(self, data: str):
        self._data = data
        self.dataChanged.emit(True)
