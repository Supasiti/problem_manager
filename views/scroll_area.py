from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from views.label import ProblemCell

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

    def __init__(self):
        super().__init__()
        self.widget = QWidget()

        grid = QGridLayout()
        grid.setSpacing(2)
        grid.setContentsMargins(0,0,0,0)

        for index in range(266):
            label = ProblemCell(96, 48, '%s' % index )
            grid.addWidget(label, index//14, index % 14)
        
        self.widget.setLayout(grid)
        self.setWidget(self.widget)