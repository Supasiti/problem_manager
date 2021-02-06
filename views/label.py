# template for fixed size/width/height label

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from models.problem_cell_data import ProblemCellData
from models.cell_data import SectorCellData

class FixedSizeLabel(QLabel):

    def __init__(self, width:int, height:int):
        super().__init__()
        self.setFixedWidth(width) 
        self.setFixedHeight(height) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 
        self.set_colours(Colour(20,20,20), Colour(240,240,240))

    def set_colours(self, 
        colour:Colour, text_colour: Colour):
        
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)


class ProblemCell(FixedSizeLabel):
    # cell displaying info on problem if there is no problem on this particular
    # cell. This is the base problem cell.

    def __init__(self, width:int, height:int, data: ProblemCellData, controller):
        super().__init__(width, height)
        self.data            = data
        self.controller      = controller
        self.clicked_command = None
        
        self.set_colours(self.data.bg_colour, self.data.text_colour)
        self.__add_mouse_effect()
        self.__add_text()

    # TODO width, height in problem cell data

    def __add_mouse_effect(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.enterEvent  = self.__add_hover_effect
        self.leaveEvent  = self.__remove_hover_effect

        if not self.clicked_command is None:
            self.mousePressEvent = self.__on_mouse_clicked
    
    def __on_mouse_clicked(self, event):
        if not self.clicked_command is None:
            self.clicked_command(self.data.id)
    
    def __add_hover_effect(self, event):
        self.set_colours(self.data.hover_colour, self.data.text_colour)
    
    def __remove_hover_effect(self, event):
        self.set_colours(self.data.bg_colour, self.data.text_colour)

    def __add_text(self):
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(2,2,2,2)
        text_style = QLabel(self.data.text)
        text_style.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        text_ric = QLabel(self.data.RIC)
        text_ric.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(text_style)
        layout.addWidget(text_ric)
        self.setLayout(layout)

    def set_clicked_command(self, command):
        self.clicked_command = command
        self.mousePressEvent = self.__on_mouse_clicked


class GradeCell(FixedSizeLabel):
    # cell displaying info related to the grade

    def __init__(self, width:int, height:int, name:str):
        super().__init__(width, height)
        self.name = name
        self.set_colours(Colour(30,30,30), Colour(240,240,240))


class SectorCell(FixedSizeLabel):
    # cell displaying info on each sector

    def __init__(self, width:int, height:int, data:SectorCellData):
        super().__init__(width, height)
        self.data = data
        self.set_colours(self.data.bg_colour, self.data.text_colour)
        self.__add_text()

    # TODO put width and height in SectorCellData

    def __add_text(self):
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(2,2,2,2)
        text_sector = QLabel(self.data.text)
        text_sector.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        text_count = QLabel(self.data.problem_count)
        text_count.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(text_sector)
        layout.addWidget(text_count)
        self.setLayout(layout)