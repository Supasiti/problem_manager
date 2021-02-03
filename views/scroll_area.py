from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from views.label import ProblemCell, GradeCell, SectorCell

class ScrollArea(QScrollArea):

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.NoFrame)   
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.set_background_colour()
    
    def set_background_colour(self):
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(20, 20, 20))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

class FixedWidthScrollArea(ScrollArea):

    def __init__(self, width):
        super().__init__()
        self.setFixedWidth(width)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

class FixedHeightScrollArea(ScrollArea):

    def __init__(self, height):
        super().__init__()
        self.setFixedHeight(height)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class ProblemScrollArea(ScrollArea):
    # area similar to excel sheet to display problem cells

    def __init__(self, n_row: int, n_columns:int, controller):
        super().__init__()
        self.controller = controller
        self.widget = QWidget()
        self.n_row = n_row
        self.n_col = n_columns
        
        grid = QGridLayout()
        grid.setSpacing(2)
        grid.setContentsMargins(0,0,0,0)

        for index in range(self.n_cells):
            label = ProblemCell(96, 48, index//self.n_col, index % self.n_col )
            label.set_clicked_command(self.controller.print_cell_info)
            grid.addWidget(label, index//self.n_col, index % self.n_col)
        
        self.widget.setLayout(grid)
        self.setWidget(self.widget)
    

    
    @property
    def n_cells(self):
        return self.n_row * self.n_col

    def connect_horizontal_scroll_bar(self, command):
        self.horizontalScrollBar().valueChanged.connect(command)
    
    def connect_vertical_scroll_bar(self, command):
        self.verticalScrollBar().valueChanged.connect(command)


class SectorScrollArea(FixedHeightScrollArea):
    # area displaying sectors in the gym

    def __init__(self, height:int, n_columns:int):
        super().__init__(height)
        self.widget = QWidget()
        self.n_col = n_columns
        self.__set_layout()
        self.__hide_scroll_bar()
    
    def __set_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0,0,0,0)

        for index in range(self.n_col):
            label = SectorCell(96, 48, '%s' % index )
            layout.addWidget(label)
        
        self.widget.setLayout(layout)
        self.setWidget(self.widget)

    def __hide_scroll_bar(self):
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
    
    def set_horizontal_bar_value(self, value: int):
        self.horizontalScrollBar().setValue(value)


class GradeScrollArea(FixedWidthScrollArea):
    # scroll area displaying grades in the gym

    def __init__(self, width:int, n_row:int):
        super().__init__(width)
        self.widget = QWidget()
        self.n_row = n_row
        self.__set_layout()
        self.__hide_scroll_bar()
    
    def __set_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0,0,0,0)

        for index in range(self.n_row):
            label = GradeCell(160, 48, '%s' % index )
            layout.addWidget(label)
        
        self.widget.setLayout(layout)
        self.setWidget(self.widget)

    def __hide_scroll_bar(self):
        self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
    
    def set_vertical_bar_value(self, value: int):
        self.verticalScrollBar().setValue(value)