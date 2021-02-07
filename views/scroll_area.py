from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from views.label import ProblemCell, GradeCell, SectorCell
from models.problem_cell_data import ProblemCellData

class ScrollArea(QScrollArea):

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.NoFrame)   
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    
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

class ProblemArea(ScrollArea):
    # area similar to excel sheet to display problem cells

    widget: QWidget
    grid: QGridLayout

    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model      = model
        
        self.__init_UI()
        self.__config_dynamic_UI()
        self.__connect_with_model()
    
    def __init_UI(self):
        self.widget     = QWidget()
        self.layout     = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

    def __config_dynamic_UI(self):
        for cell_data in self.model.changes.cells:
            self.__generate_cell(cell_data, 96, 48)
        
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def __generate_cell(self, cell_data: ProblemCellData, width: int, height:int):
        cell  = ProblemCell(width, height, cell_data)
    #     cell.set_clicked_command(self.controller.print_cell_info)
        self.layout.addWidget(cell, cell_data.row, cell_data.col)

    def connect_horizontal_scroll_bar(self, command):
        self.horizontalScrollBar().valueChanged.connect(command)
    
    # def connect_vertical_scroll_bar(self, command):
    #     self.verticalScrollBar().valueChanged.connect(command)
    
    def __connect_with_model(self):
        self.model.cellsChanged.connect(self.__config_dynamic_UI)
    

class SectorArea(FixedHeightScrollArea):
    # area displaying sectors in the gym

    widget : QWidget
    n_col : int 

    def __init__(self, controller, model, height:int=48):
        self.controller = controller
        self.model     = model
        self.height    = height
        super().__init__(self.height)
        
        self.__init_UI()
        self.__config_dynamic_UI()
        self.__hide_scroll_bar()
        self.__connect_with_model()
    
    def __init_UI(self):
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

    def __config_dynamic_UI(self):
        for cell_data in self.model.changes.cells:
            self.__generate_cell(cell_data, self.height)

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def __generate_cell(self, cell_data: ProblemCellData, height:int):
        cell  = SectorCell(height, cell_data)
    #     cell.set_clicked_command(self.controller.print_cell_info)
        self.layout.addWidget(cell, 0, cell_data.col)

    def __hide_scroll_bar(self):
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
    
    def set_horizontal_bar_value(self, value: int):
        self.horizontalScrollBar().setValue(value)
    
    def __connect_with_model(self):
        self.model.cellsChanged.connect(self.__config_dynamic_UI)


class GradeArea(FixedWidthScrollArea):
    # scroll area displaying grades in the gym

    widget : QWidget
    n_row  : int 

    def __init__(self, n_row:int, width:int=160 ):
        super().__init__(width)
        
        self.width = width
        self.n_row = n_row
        self.__init_layout()
        self.__hide_scroll_bar()
    
    def __init_layout(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.__config_layout()
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def __config_layout(self):
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

        for row in range(self.n_row - 1 ):
            self.__generate_cell(row, self.width, 48)
        self.__generate_cell(self.n_row - 1, self.width, 62)

    def __generate_cell(self, row:int, width: int, height: int):
        label = GradeCell(width, height, 'model' )
        self.layout.addWidget(label)

    def __hide_scroll_bar(self):
        self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
    
    def set_vertical_bar_value(self, value: int):
        self.verticalScrollBar().setValue(value)