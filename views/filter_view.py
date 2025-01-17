from __future__ import annotations
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QDateEdit, QSizePolicy, QPushButton
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from PyQt5.QtCore import Qt 

from views.label import FixedWidthLabel, FixedSizeLabel

class FilterView(FixedWidthLabel):

    def __init__(self, controller, model): 
        self.controller = controller
        self.model      = model
        self.width      = self.model.static_data.width
        super().__init__(self.width)

        self._init_UI()

    def _init_UI(self) -> None:
        data = self.model.static_data
        self.layout = QVBoxLayout()
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(8,2,8,2)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.title = FixedSizeLabel(self.width -6, 40, 'Problem Filter')
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title.set_colours(data.bg_colour, data.text_colour)

        self.dateedit_start = QDateEdit()
        self.dateedit_start.setCalendarPopup(True)
        self.dateedit_start.userDateChanged.connect(self._on_start_date_changed)
        self.dateedit_end   = QDateEdit()
        self.dateedit_end.setCalendarPopup(True)
        self.dateedit_end.userDateChanged.connect(self._on_end_date_changed)

        self.layout_date = QFormLayout()
        self.layout_date.setFormAlignment(Qt.AlignTop)
        self.layout_date.setLabelAlignment(Qt.AlignRight)
        self.layout_date.setContentsMargins(2,2,2,2)
        self.layout_date.setSpacing(4)

        self.layout_date.addRow('Start Date:', self.dateedit_start)
        self.layout_date.addRow('End Date :',  self.dateedit_end )

        self.layout_RIC = QHBoxLayout()
        self.layout_RIC.setSpacing(4)
        self.layout_RIC.setContentsMargins(0,0,0,0)
        self.layout_RIC.setAlignment(Qt.AlignTop)

        self.layout_other = QGridLayout()
        self.layout_other.setSpacing(4)
        self.layout_other.setContentsMargins(0,0,0,0)
        self.layout_other.setAlignment(Qt.AlignTop)

        self.button_reset = QPushButton('Reset')
        self.button_reset.clicked.connect(self._reset_filters)

        self.layout.addWidget(self.title)
        self.layout.addLayout(self.layout_date)
        self.layout.addLayout(self.layout_RIC)
        self.layout.addLayout(self.layout_other)
        self.layout.addWidget(self.button_reset)
        self._add_all_widgets()

    def set_data(self, arg:bool) -> None:
        self._remove_all_widgets()
        self._add_all_widgets()
    
    def _add_all_widgets(self) -> None:
        self._add_RIC_widgets()
        self._add_other_widgets()

    def _add_RIC_widgets(self) -> None:
        if len(self.model.views) >= 3:
            for widget in self.model.views[0:3]:
                self.layout_RIC.addWidget(widget, alignment=Qt.AlignTop)

    def _add_other_widgets(self) -> None:
        if len(self.model.views) >= 3:
            for index, widget in enumerate(self.model.views[3:]):
                self.layout_other.addWidget(widget, index // 2, index % 2, alignment=Qt.AlignTop)

    def _remove_all_widgets(self) -> None:
        self._remove_widgets_from(self.layout_RIC)
        self._remove_widgets_from(self.layout_other)

    def _remove_widgets_from(self, layout:QLayout) -> None:
        for index in reversed(range(layout.count())):
            widget = layout.itemAt(index).widget()
            layout.removeWidget(widget)
            widget.setParent(None)

    def _on_start_date_changed(self, date)-> None:
        self.controller.on_start_date_changed(date)
    
    def _on_end_date_changed(self, date)-> None:
        self.controller.on_end_date_changed(date)

    def set_min_date(self, date) -> None:
        self.dateedit_start.setMinimumDate(date)
        self.dateedit_end.setMinimumDate(date)
        self.dateedit_start.setDate(date)

    def set_max_date(self, date) -> None:
        self.dateedit_start.setMaximumDate(date)
        self.dateedit_end.setMaximumDate(date)
        self.dateedit_end.setDate(date)

    def _reset_filters(self) -> None:
        min_date = self.dateedit_start.minimumDate()
        self.dateedit_start.setDate(min_date)
        max_date = self.dateedit_end.maximumDate()
        self.dateedit_end.setDate(max_date)
        self._unselect_all_widgets_in(self.layout_RIC)
        self._unselect_all_widgets_in(self.layout_other)
        self.controller.reset()
    
    def _unselect_all_widgets_in(self, layout:QLayout) -> None:
        for index in reversed(range(layout.count())):
            widget = layout.itemAt(index).widget()
            widget.clear_selection()


class BaseFilterView(QLabel):

    def __init__(self, controller, model): 
        super().__init__()
        self.controller = controller
        self.model      = model
        self._init_UI()
    
    def _init_UI(self):
        self.setFixedHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.list_view = QListWidget()
        self.list_view.setFixedHeight(100)
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_view.itemSelectionChanged.connect(self._on_item_selected)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list_view)

    
    def set_title(self, text:str) -> None:
        self.title.setText(text)

    def set_items(self, texts:tuple[str,...]) ->None:
        self.list_view.clear()
        for text in texts:
            self._add_item(text)

    def _add_item(self, text:str) -> None:
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignHCenter)
        self.list_view.addItem(item) 

    def _on_item_selected(self) ->None:
        selected = [item.text() for item in self.list_view.selectedItems()]
        self.controller.on_item_selected(selected)

    def clear_selection(self) -> None:
        self.list_view.clearSelection()
        