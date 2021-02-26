from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
from views.frame import Frame
from views.list_cell import ListCell

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour

class ProblemListView(Frame):

    scrollarea  : QScrollArea
    widget      : QWidget
    list_layout : QVBoxLayout

    def __init__(self, controller, model):
        super().__init__()
        self.controller   = controller
        self.model        = model
        self._init_UI()
        self._connect_other()

    def _init_UI(self):
        layout = QGridLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0,0,0,0)
        
        self.scrollarea  = QScrollArea()
        self.widget      = QLabel('')
        self.widget.setFixedWidth(400)
        self.widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.set_colours(self.widget,Colour(255,0,0),Colour(0,0,0))
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(2)
        self.list_layout.setContentsMargins(10,0,10,0)
        self.list_layout.setAlignment(Qt.AlignTop)
    
        self.widget.setLayout(self.list_layout)
        self.scrollarea.setWidget(self.widget)

        layout.addWidget(self.scrollarea, 0,0)
        self.setLayout(layout)

    def set_data(self, arg:bool):
        self._clear_list()
        for cell in self.model.data:
            self.list_layout.addWidget(ListCell(cell))
      


    def _clear_list(self):
        for i in reversed(range(self.list_layout.count())): 
            self.list_layout.itemAt(i).widget().setParent(None)

    def _connect_other(self):
        self.model.cellsChanged.connect(self._init_UI)

    def set_colours(self, element,
        colour: Colour, text_colour: Colour):
        
        element.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        element.setPalette(pal)