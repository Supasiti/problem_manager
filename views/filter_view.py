from __future__ import annotations
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy, QLayout
from PyQt5.QtWidgets import QLabel
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

        self.layout_RIC = QHBoxLayout()
        self.layout_RIC.setSpacing(4)
        self.layout_RIC.setContentsMargins(0,0,0,0)
        self.layout_RIC.setAlignment(Qt.AlignTop)

        self.layout_other = QGridLayout()
        self.layout_other.setSpacing(4)
        self.layout_other.setContentsMargins(0,0,0,0)
        self.layout_other.setAlignment(Qt.AlignTop)

        self.layout.addWidget(self.title)
        self.layout.addLayout(self.layout_RIC)
        self.layout.addLayout(self.layout_other)
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
        # self.list_view.hide()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list_view)

        # self.title.mousePressEvent = self._toggle_list_view_visibility
    
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

    # def _toggle_list_view_visibility(self, event) -> None:
    #     if self.list_view.isHidden():
    #         self.list_view.setFixedHeight(100)
    #         self.list_view.show()
    #     else:
    #         # self.list_view.setFixedHeight(0)
    #         self.list_view.hide()