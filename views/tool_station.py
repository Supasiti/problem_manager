from PyQt5.QtWidgets import QLabel
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
        self._set_data()
        self._connect_model()

    def _init__UI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(1,1,1,1)


        self.seperator = FixedSizeLabel(self.width - 12, 1)
        self.seperator.set_colours(Colour(240,240,240), Colour(240,240,240))

    def _set_data(self):
        data        = self.model.view_data
        
        self.editor = data.editor

        self.layout.addWidget(self.editor,    alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.seperator, alignment=Qt.AlignHCenter)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def _connect_model(self):
        self.model.dataChanged.connect(self._set_data)
        return True

        