from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from services.colour_setting import ColourSetting
from APImodels.colour import Colour
from APImodels.problem import Problem

class ProblemListStaticData(NamedTuple):

    bg_colour   : Colour  = Colour(45,45,45)
    text_colour : Colour = Colour(240,240,240)

class ProblemListData(NamedTuple):
    cells : list = list()

class ProblemListDataBuilder():
    
    def __init__(self, colour_setting: ColourSetting):
        self._setting = colour_setting
        self._builder = ProblemListCellDataBuilder(self._setting)

    def from_problems(self, problems:tuple[Problem,...]) -> ProblemListData:
        cells = [self._builder.from_row(i,p) for i, p in enumerate(problems)]
        return ProblemListData(cells)

class ProblemListModel(QObject):

    cellsChanged = pyqtSignal(bool)

    def __init__(self,
        static_data: ProblemListStaticData = ProblemListStaticData(), 
        data : ProblemListData = ProblemListData()):
        super().__init__()
        self._static_data = static_data
        self._data = data
    
    @property
    def static_data(self) -> ProblemListStaticData:
        return self._static_data

    @property
    def data(self) -> list:
        return self._data.cells

    @data.setter
    def data(self, value: ProblemListData) -> None :
        self._data = value
        self.cellsChanged.emit(True)


class ProblemListCellData(NamedTuple):

    row   : int
    problem : Problem
    bg_colour : Colour
    text_colour : Colour
    hover_colour : Colour
    height : int = 36

class ProblemListCellDataBuilder():

    def __init__(self, colour_setting: ColourSetting):
        self._setting = colour_setting

    def from_row(self, row:int, problem:Problem) -> ProblemListCellData:

        colour = 'default' if row %2 == 0 else 'default_light'
        bg_colour = self._setting.get_bg_colour(colour)
        text_colour = self._setting.get_text_colour(colour)
        hover_colour = self._setting.get_hover_colour(colour)

        return ProblemListCellData(row, problem, bg_colour, text_colour, hover_colour)