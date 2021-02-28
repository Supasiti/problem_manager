from __future__ import annotations
from typing import NamedTuple
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from services.colour_setting import ColourSetting
from APImodels.colour import Colour
from APImodels.problem import Problem

class ProblemListCellData(NamedTuple):

    row   : int
    bg_colour : Colour
    text_colour : Colour
    hover_colour : Colour
    height : int = 36
    width  : int = 840
    header : bool = False 

class ProblemListCellDataBuilder():

    def __init__(self, colour_setting: ColourSetting):
        self._setting = colour_setting

    def from_row(self, row:int) -> ProblemListCellData:

        colour = 'default' if row %2 == 0 else 'default_light'
        bg_colour    = self._setting.get_bg_colour(colour)
        text_colour  = self._setting.get_text_colour(colour)
        hover_colour = self._setting.get_hover_colour(colour)

        return ProblemListCellData(row, bg_colour, text_colour, hover_colour)
    
    def header(self):

        bg_colour    = self._setting.get_bg_colour('default_light')
        text_colour  = self._setting.get_text_colour('default_light')
        hover_colour = self._setting.get_hover_colour('default_light')

        return ProblemListCellData(0, bg_colour, text_colour, hover_colour, header=True)


class ProblemListStaticData(NamedTuple):

    bg_colour   : Colour = Colour(45,45,45)
    text_colour : Colour = Colour(240,240,240)


class ProblemListData(NamedTuple):
    bg_colour   : Colour = Colour(45,45,45)
    text_colour : Colour = Colour(240,240,240)
    header   : ProblemListCellData = ProblemListCellData(0, Colour(45,45,45), Colour(240,240,240), Colour(60,60,60), header=True)
    even_row : ProblemListCellData = ProblemListCellData(0, Colour(30,30,30), Colour(240,240,240), Colour(60,60,60))
    odd_row  : ProblemListCellData = ProblemListCellData(1, Colour(45,45,45), Colour(240,240,240), Colour(60,60,60))
    problems : list = list()

class ProblemListDataBuilder():
    
    def __init__(self, colour_setting: ColourSetting):
        self._setting = colour_setting
        self._builder = ProblemListCellDataBuilder(self._setting)

    def from_problems(self, problems:tuple[Problem,...]) -> ProblemListData:

        bg_colour    = self._setting.get_bg_colour('default_light')
        text_colour  = self._setting.get_text_colour('default_light')
        header   = self._builder.header()
        even_row = self._builder.from_row(0)
        odd_row  = self._builder.from_row(1)

        return ProblemListData(bg_colour, text_colour, header, even_row, odd_row, problems)

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
        return self._data

    @data.setter
    def data(self, value: ProblemListData) -> None :
        self._data = value
        self.cellsChanged.emit(True)

