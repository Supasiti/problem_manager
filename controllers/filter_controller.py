from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt 

from services.dependency_service import DependencyService
from services.old_problem_viewer import OldProblemViewer
from models.filter_view_model import FilterSelectorModel, BaseFilterModel
from views.filter_view import FilterView, BaseFilterView

class BaseFilterController(ABC):

    _dependency     : DependencyService

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        self.model = BaseFilterModel()                  # load model
        self.view  = BaseFilterView(self, self.model)   # load view
        self.set_title()
        self._connect()
        self.show_available_filters()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency  = dependency
        self.viewer      = self._dependency.get(OldProblemViewer)

    def _connect(self):
        self.model.itemsChanged.connect(self.view.set_items) 

    @abstractmethod
    def set_title(self) -> None:
        pass

    @abstractmethod
    def show_available_filters(self) ->None:
        pass

    @abstractmethod  
    def on_item_selected(self, items:list[str]) -> None :
        pass


class RiskFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('R')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(r) for r in self.viewer.get_risks()])

    def on_item_selected(self, items:list[str]) -> None :
        risks = [int(item) for item in items]
        self.viewer.set_filter_R(risks)
        self.viewer.filter_problems()


class IntensityFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('I')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(r) for r in self.viewer.get_intensities()])

    def on_item_selected(self, items:list[str]) -> None :
        intensities = [int(item) for item in items]
        self.viewer.set_filter_I(intensities)
        self.viewer.filter_problems()


class ComplexityFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('C')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(r) for r in self.viewer.get_complexities()])

    def on_item_selected(self, items:list[str]) -> None :
        complexities = [int(item) for item in items]
        self.viewer.set_filter_C(complexities)
        self.viewer.filter_problems()


class ColourFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('Hold Colour')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(h) for h in self.viewer.get_holds()])

    def on_item_selected(self, items:list[str]) -> None :
        self.viewer.set_filter_holds(items)
        self.viewer.filter_problems()


class GradeFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('Grade')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(h) for h in self.viewer.get_grades()])

    def on_item_selected(self, items:list[str]) -> None :
        self.viewer.set_filter_grades(items)
        self.viewer.filter_problems()


class SectorFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('Sector')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(h).upper() for h in self.viewer.get_sectors()])

    def on_item_selected(self, items:list[str]) -> None :
        sectors = [item.lower() for item in items]
        self.viewer.set_filter_sectors(sectors)
        self.viewer.filter_problems()


class StyleFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('Style')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(h) for h in self.viewer.get_styles()])

    def on_item_selected(self, items:list[str]) -> None :
        self.viewer.set_filter_styles(items)
        self.viewer.filter_problems()


class SetterFilterController(BaseFilterController):

    def set_title(self) -> None:
        self.view.set_title('Setter')

    def show_available_filters(self) ->None:
        self.model.items = tuple([ str(h) for h in self.viewer.get_setters()])

    def on_item_selected(self, items:list[str]) -> None :
        self.viewer.set_filter_setters(items)
        self.viewer.filter_problems()


class FilterController():
    
    _dependency   : DependencyService
    _controllers = tuple()
    _filters = (
        RiskFilterController, IntensityFilterController, ComplexityFilterController, 
        GradeFilterController, ColourFilterController, SectorFilterController, 
        StyleFilterController, SetterFilterController
    )

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        self.model = FilterSelectorModel()            # load model
        self.view  = FilterView(self, self.model)     # load view
        self._connect()
        self._set_min_max_date()
        self._show_filters()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency  = dependency
        self._viewer      = self._dependency.get(OldProblemViewer)

    def _connect(self):
        self.model.viewsChanged.connect(self.view.set_data) 
        self.model.minDateChanged.connect(self.view.set_min_date)
        self.model.maxDateChanged.connect(self.view.set_max_date)

    def _set_min_max_date(self) ->None:
        set_dates = list(self._viewer.get_set_dates())
        self.model.set_max_date(max(set_dates))
        self.model.set_min_date(min(set_dates))

    def _show_filters(self) -> None:
        self._controllers = tuple([controller(self._dependency) for controller in self._filters ])
        self.model.views  = tuple([controller.view for controller in self._controllers])

    def on_start_date_changed(self, _date:QDate) -> None:
        iso_date = _date.toString(Qt.ISODate) 
        self._viewer.set_filter_start_date(date.fromisoformat(iso_date))
        self._viewer.filter_problems()

    def on_end_date_changed(self, _date:QDate) -> None:
        iso_date = _date.toString(Qt.ISODate) 
        self._viewer.set_filter_end_date(date.fromisoformat(iso_date))
        self._viewer.filter_problems()