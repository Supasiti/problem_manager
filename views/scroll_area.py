from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
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

    widget: QWidget
    grid: QGridLayout
    n_row: int
    n_col: int

    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model  = model
        
        self.__init_grid()
        self.__connect_with_model()
    
    def __init_grid(self):
        self.widget     = QWidget()
        self.grid       = QGridLayout()
        self.__config_grid()
        self.widget.setLayout(self.grid)
        self.setWidget(self.widget)

    def __config_grid(self):
        self.grid.setSpacing(2)
        self.grid.setContentsMargins(0,0,0,0)
        self.n_row = self.model.n_row
        self.n_col = self.model.n_col

        for index in range(self.n_cells):
            self.__generate_problem_cell(index)
            
    def __generate_problem_cell(self, index:int):
        row   = index//self.n_col
        col   = index % self.n_col
        model = self.__get_cell_model(row, col)
        cell  = ProblemCell(96, 48, model, self.controller)
        cell.set_clicked_command(self.controller.print_cell_info)
        self.grid.addWidget(cell, row, col)
        
    def __get_cell_model(self, row, col):
        if (row, col) in self.model.cell_models.keys():
            return self.model.cell_models[(row,col)]     
        return self.model.get_default_problem_cell_model(row, col)
        
    @property
    def n_cells(self):
        return self.n_row * self.n_col

    def connect_horizontal_scroll_bar(self, command):
        self.horizontalScrollBar().valueChanged.connect(command)
    
    def connect_vertical_scroll_bar(self, command):
        self.verticalScrollBar().valueChanged.connect(command)
    
    def __connect_with_model(self):
        self.model.cellModelsChanged.connect(self.__init_grid)
    

class SectorScrollArea(FixedHeightScrollArea):
    # area displaying sectors in the gym

    def __init__(self, n_columns:int, height:int=48,):
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

    def __init__(self, n_row:int, width:int=160 ):
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