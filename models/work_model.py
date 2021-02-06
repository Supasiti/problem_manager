#  Model for the work station
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from views.scroll_area import ProblemArea, SectorArea, GradeArea
from views.info_area import InfoArea
from APImodels.colour import Colour

class WorkStaticData(NamedTuple):

    bg_colour    : Colour
    
    @staticmethod
    def default():
        return WorkStaticData(Colour(45,45,45))

class WorkDynamicData(NamedTuple):
    info_view    : InfoArea
    sector_view  : SectorArea
    grade_view   : GradeArea
    problem_view : ProblemArea

    @staticmethod
    def default():
        return WorkDynamicData(None, None, None, None)

class WorkStationModel(QObject):

    dataChanged = pyqtSignal(bool)

    def __init__(self,
        static_data  : WorkStaticData = WorkStaticData.default(),
        dynamic_data : WorkDynamicData = WorkDynamicData.default()
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
        self.dataChanged.emit(value)