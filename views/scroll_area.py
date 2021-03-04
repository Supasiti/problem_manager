from PyQt5.QtWidgets import *
from PyQt5.QtCore import QMargins
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from views.label import ProblemCell, GradeCell, SectorCell, InfoCell
from models.problem_cell_data import ProblemCellData
from models.sector_area_model import SectorCellData

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
    layout: QGridLayout

    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model      = model
        
        self._init_UI()
        self._connect_scroll_bars()
    
    def _init_UI(self):
        self.panels   = self.model.panels
        self.margins  = QMargins(self.panels.left_margin, self.panels.top_margin, 0, 0)
        self.setViewportMargins(self.margins)

        self.header     = self.panels.sector_view
        self.left_panel = self.panels.grade_view
        self.info_panel = self.panels.info_view
        self.header.setParent(self)
        self.left_panel.setParent(self)
        self.info_panel.setParent(self)

        self.widget     = QWidget()
        self.layout     = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        for cell_data in self.model.changes.cells:
            self._generate_cell(cell_data, 96, 48)

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def _generate_cell(self, cell_data: ProblemCellData, width: int, height:int):
        cell  = ProblemCell(width, height, cell_data)
        cell.set_clicked_command(self.controller.on_cell_clicked)
        self.layout.addWidget(cell, cell_data.row, cell_data.col)

    def _connect_scroll_bars(self):
        self.horizontalScrollBar().valueChanged.connect(lambda x : self.header.horizontalScrollBar().setValue(x))
        self.header.horizontalScrollBar().valueChanged.connect(lambda x : self.horizontalScrollBar().setValue(x))
        self.verticalScrollBar().valueChanged.connect(lambda x : self.left_panel.verticalScrollBar().setValue(x))
        self.left_panel.verticalScrollBar().valueChanged.connect(lambda x : self.verticalScrollBar().setValue(x))
    
    def set_cell_data(self):
        for cell_data in self.model.changes.cells:
            cell = self.layout.itemAtPosition(cell_data.row, cell_data.col).widget()
            cell.set_data(cell_data)

    def resizeEvent(self, event):
        rect = self.viewport().geometry()
        self.header.setGeometry(
            rect.x(), 0, rect.width(), self.margins.top()-4
            )
        self.left_panel.setGeometry(
            0, rect.y(), self.margins.left()-4, rect.height()
        )
        QScrollArea.resizeEvent(self, event)

class SectorArea(FixedHeightScrollArea):
    # area displaying sectors in the gym

    widget : QWidget

    def __init__(self, controller, model):
        self.controller = controller
        self.model     = model
        self.height    = self.model.changes.height
        super().__init__(self.height)
        
        self._init_UI()
        self._hide_scroll_bar()
    
    def _init_UI(self):
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        for cell_data in self.model.changes.cells:
            self._generate_cell(cell_data, self.height)

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

    def _generate_cell(self, cell_data: SectorCellData, height:int):
        cell  = SectorCell(height, cell_data)
        self.layout.addWidget(cell, 0, cell_data.col)

    def _hide_scroll_bar(self):
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
    
    def set_cell_data(self):
        for cell_data in self.model.changes.cells:
            cell = self.layout.itemAtPosition(0, cell_data.col).widget()
            cell.set_data(cell_data)


class GradeArea(FixedWidthScrollArea):
    # scroll area displaying grades in the gym

    widget : QWidget

    def __init__(self, controller, model):
        self.controller = controller
        self.model      = model
        self.width      = self.model.static.width
        super().__init__(self.width)
        
        self._init_UI()
        self._hide_scroll_bar()
    
    def _init_UI(self):
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        
        for cell_data in self.model.static.cells:
            count = self.model.counts.get_cell(cell_data.row)
            self.layout.addWidget(GradeCell(cell_data, count), cell_data.row, 0)
        
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
     
    def _hide_scroll_bar(self):
        self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")

    def set_count_data(self):
        for count_data in self.model.counts.cells:
            cell = self.layout.itemAtPosition(count_data.row, 0).widget()
            cell.set_count_data(count_data)
