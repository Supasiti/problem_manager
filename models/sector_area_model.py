from __future__ import annotations
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import NamedTuple

from services.setting import Setting
from services.colour_setting import ColourSetting
from services.sector_editor import SectorEditor
from APImodels.sector import Sector
from APImodels.problem import Problem
from APImodels.colour import Colour

class SectorCellData(NamedTuple):
    # cell model containing data for sector cell

    col   : int
    width : int
    bg_colour : Colour
    text_colour : Colour
    text : str
    problem_count : str


class SectorCellDataBuilder():
    # build sector cell data from either:
    #  - sectors
    #  - col - in case there isn't one

    def __init__(self, sector_editor:SectorEditor):
        self.sector_setting = sector_editor
        self.colour_setting = Setting.get(ColourSetting)

    def from_sector(self, sector:Sector):

        col   = self.sector_setting.get_col(sector.name)
        width = 96 
        text  = sector.name.upper()
        count = str(sector.count)
        bg_colour   = self._background_colour(sector.setting)
        text_colour = self._text_colour(sector.setting)
    
        return SectorCellData(col, width, bg_colour, text_colour, text, count)

    def _background_colour(self, setting:bool):
        colour_str = 'setting' if setting else 'default'
        return self.colour_setting.get_bg_colour(colour_str) 

    def _text_colour(self, setting:bool):
        colour_str = 'setting' if setting else 'default'
        return self.colour_setting.get_text_colour(colour_str)
    
    def from_col(self, col:int):
        width        = 96 
        text         = self.sector_setting.get_sector(col).upper()
        bg_colour    = self._background_colour(False)
        text_colour  = self._text_colour(False)

        return SectorCellData(col, width, bg_colour, text_colour, text, '0') 


class SectorAreaData(NamedTuple):
    cells  : tuple[SectorCellData,...]
    n_col  : int
    height : int = 48
    
class SectorAreaDataBuilder():
   
    def __init__(self, sector_editor:SectorEditor):
        self._builder        = SectorCellDataBuilder(sector_editor)
        self._sector_setting = sector_editor

    @property
    def n_col(self) -> int:
        return self._sector_setting.length()

    @property
    def sectors(self) -> tuple:
        return self._sector_setting.get_all_sectors()

    def default(self):
        cells = [self._builder.from_col(index) for index in range(self.n_col)]
        cells.sort(key= lambda x : x.col)
        return SectorAreaData(tuple(cells), self.n_col)

    def from_problems(self, problems:tuple[Problem,...]):
        prob = tuple(problems)
        if len(prob) == 0 :
            return self.default()
        set_date = self._last_setting_date(prob)
        sectors  = [Sector.from_problems(s, prob, set_date) for s in self.sectors]
        cells    = list([self._builder.from_sector(s) for s in sectors ])
        cells.sort(key= lambda x : x.col)
        return SectorAreaData(tuple(cells), self.n_col)

    def _last_setting_date(self, problems:tuple[Problem,...]):
        prob = tuple(problems)
        if len(prob) == 0: 
            raise ValueError('_get_last_setting_date() don\'t accept empty generator')
        return max([p.set_date for p in prob]) 


class SectorAreaModel(QObject):
    
    cellsChanged = pyqtSignal(bool)
    _changes : SectorAreaData

    def __init__(self, sector_editor:SectorEditor):
        super().__init__()
        self._builder = SectorAreaDataBuilder(sector_editor)
        self._data   = self._builder.default()
        self.changes = self._builder.default()

    @property
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, value: SectorAreaData):
        self._update_data(value)
        self._changes = value
        self.cellsChanged.emit(True)

    def _update_data(self, value: SectorAreaData):
        old_data  = list(self._data.cells)
        new_data  = list(value.cells)
        new_cells = [d.col for d in new_data]
        old_data_to_retain = [ d for d in old_data if not d.col in new_cells]
        new_data += old_data_to_retain
        self._data = SectorAreaData(tuple(new_data), value.n_col)

    def problems_changed(self, problems: tuple[Problem,...]) -> None:
        self.changes = self._builder.from_problems(problems)