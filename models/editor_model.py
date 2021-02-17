# Problem editor  model
# 
# contains all the informations being presented in Problem Editor
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from APImodels.problem import Problem

class EditorStaticData(NamedTuple):

    width      : int
    height     : int

    @staticmethod
    def default():
        return EditorStaticData(276, 460)

class EditorData(NamedTuple):

    holds : tuple[str]
    problem : Problem
    are_buttons_visible : bool

class EditorModel(QObject):
    
    dataChanged = pyqtSignal(bool) 

    def __init__(self, 
        static_data  : EditorStaticData = EditorStaticData.default(),
        dynamic_data : EditorData = None 
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
    def dynamic_data(self, data: str):
        self._dynamic_data = data
        self.dataChanged.emit(True)