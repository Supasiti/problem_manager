from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from views.frame import FixedWidthFrame
from views.label import FixedSizeLabel

class ToolStation(FixedWidthFrame):
  
    def __init__(self, controller, model):
        self.controller = controller
        self.model      = model
        self.width      = self.model.view_data.width
        super().__init__(self.width)
    
        self._init__UI()

    def _init__UI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(1,1,1,1)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)
        self._add_all_widgets()

    def set_data(self):
        self._remove_all_widgets()
        self._add_all_widgets()

    def _add_all_widgets(self) -> None:
        widgets  = self.model.view_data.tools
        for widget in widgets:
            seperator = FixedSizeLabel(self.width - 12, 1)
            seperator.set_colours(Colour(240,240,240), Colour(240,240,240))
            self.layout.addWidget(widget,    alignment=Qt.AlignHCenter)
            self.layout.addWidget(seperator, alignment=Qt.AlignHCenter)

    def _remove_all_widgets(self) -> None:
        for index in reversed(range(self.layout.count())):
            self.layout.removeWidget(self.layout.itemAt(index).widget())

        