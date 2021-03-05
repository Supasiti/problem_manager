from __future__ import annotations
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt 
from typing import NamedTuple
from datetime import date

from services.setting import Setting
from services.colour_setting import ColourSetting
from APImodels.colour import Colour

class FilterViewStaticData(NamedTuple):

    width       : int = 276
    bg_colour   : Colour = Setting.get(ColourSetting).get_bg_colour('default')
    text_colour : Colour = Setting.get(ColourSetting).get_text_colour('default')

class FilterSelectorModel(QObject):
    
    viewsChanged = pyqtSignal(bool)
    minDateChanged = pyqtSignal(QDate)
    maxDateChanged = pyqtSignal(QDate)
    _views = tuple()

    def __init__(self):
        super().__init__()
        self.static_data = FilterViewStaticData()
        self.views    = tuple()
        self.min_date = QDate(2000,1,1)
        self.max_date = QDate(2000,1,1)

    @property
    def views(self):
        return self._views
    
    @views.setter
    def views(self, data: tuple):
        self._views = data
        self.viewsChanged.emit(True)

    def set_min_date(self, min_date:date) -> None:
        self.min_date = QDate.fromString(min_date.isoformat(), Qt.ISODate)
        self.minDateChanged.emit(self.min_date)
    
    def set_max_date(self, max_date:date) -> None:
        self.max_date = QDate.fromString(max_date.isoformat(), Qt.ISODate)
        self.maxDateChanged.emit(self.max_date)

class BaseFilterModel(QObject):

    itemsChanged = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self._items = tuple()

    @property
    def items(self):
        return self._items
    
    @items.setter
    def items(self, data: tuple):
        self._items = data
        self.itemsChanged.emit(data)