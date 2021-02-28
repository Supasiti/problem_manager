from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel
from views.frame import Frame
from views.list_cell import ListCell

from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from views.list_cell import ListCellHeader, ListCell

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
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(10,0,10,0)
        layout.setAlignment(Qt.AlignTop) 
        
        self.title = QLabel('Problem List')
        self.title.setFont(QFont('.AppleSystemUIFont', 28))
        self.title.setMargin(20)

        self.header_scrollarea  = QScrollArea()
        self.header_scrollarea.setWidgetResizable(True)
        self.header     = ListCellHeader(self.model.data.header)
        self.header.set_clicked_command(self.controller.sort_by)
        self.header_layout = QVBoxLayout()
        self.header_layout.setContentsMargins(0,0,0,0)
        self.header_layout.setAlignment(Qt.AlignTop) 
        self.header_layout.addWidget(self.header)
        

        self.scrollarea  = QScrollArea()
        self.scrollarea.setWidgetResizable(True)  # so scrollarea can adjust size with child widget
        self.widget      = QWidget(parent=self)
        
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(2)
        self.list_layout.setContentsMargins(0,0,0,0)
        self.list_layout.setAlignment(Qt.AlignTop) 

        self.widget.setLayout(self.list_layout)
        self.scrollarea.setWidget(self.widget)
        layout.addWidget(self.title)
        layout.addWidget(self.header )
        layout.addWidget(self.scrollarea)
        self.setLayout(layout)

    def set_data(self, arg:bool):
        self._set_colours(self.model.data.bg_colour, self.model.data.text_colour)
        
        self._setup_rows()
        self._set_problem_data()

    def _setup_rows(self):
        n_problems = len(self.model.data.problems)
        n_rows     = self.list_layout.count()
        if n_rows > n_problems:
            self._remove_rows(n_problems, n_rows)
        if n_problems > n_rows:
            self._add_rows(n_rows, n_problems)

    def _add_rows(self, start:int, end:int) ->None:
        for i in range(end)[start:]:
            cell_data = self.model.data.even_row if i % 2 ==0 else self.model.data.odd_row
            self.list_layout.addWidget(ListCell(cell_data))
    
    def _remove_rows(self, start:int, end:int ) ->None:
        for i in reversed(range(end)[start:]):
            self.list_layout.itemAt(i).widget().setParent(None)
    
    def _set_problem_data(self) -> None:
        for i,problem in enumerate(self.model.data.problems):
            self.list_layout.itemAt(i).widget().set_problem_data(problem) 

    def _connect_other(self):
        self.model.cellsChanged.connect(self.set_data)

    def _set_colours(self, colour: Colour, text_colour: Colour):
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)