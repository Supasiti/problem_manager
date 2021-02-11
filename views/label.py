# template for fixed size/width/height label

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from models.problem_cell_data import ProblemCellData
from models.cell_data import SectorCellData, GradeCellData, GradeCountData

class FixedSizeLabel(QLabel):

    def __init__(self, width:int, height:int, text:str=''):
        super().__init__(text)
        self.setFixedWidth(width) 
        self.setFixedHeight(height) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 

    def set_colours(self, 
        colour: Colour, text_colour: Colour):
        
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)


class ProblemCell(FixedSizeLabel):
    # cell displaying info on problem if there is no problem on this particular
    # cell. This is the base problem cell.

    def __init__(self, width:int, height:int, data: ProblemCellData):
        super().__init__(width, height)
        self.data            = data
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
            self.clicked_command(self.data.id, self.data.row, self.data.col)
    
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

    def __init__(self, data : GradeCellData):
        super().__init__(data.width, data.height)
        self.data  = data

        self.__init_UI()

    def __init_UI(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

        self.text_style = FixedSizeLabel(self.data.inner_width, self.data.inner_height)
        self.text_style.setText('Style')
        self.text_style.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.text_style.set_colours(self.data.bg_colour, self.data.text_colour)

        self.text_ric = FixedSizeLabel(self.data.inner_width, self.data.inner_height)
        self.text_ric.setText('RIC')
        self.text_ric.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        self.text_ric.set_colours(self.data.bg_colour, self.data.text_colour)

        self.text_aim = FixedSizeLabel(self.data.inner_width, self.data.height)
        self.text_aim.setText(self.data.aim)
        self.text_aim.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        self.text_aim.set_colours(self.data.bg_colour, self.data.text_colour)

        self.layout.addWidget(self.text_style, 0, 0)
        self.layout.addWidget(self.text_ric,   1, 0)
        self.layout.addWidget(self.text_aim,   0, 1, 1, 2)
        self.setLayout(self.layout)

class GradeCountCell(FixedSizeLabel):

    def __init__(self, data : GradeCountData):
        super().__init__(data.width, data.height)
        self.data  = data

        self.__init_UI()

    def __init_UI(self):
        self.setText(self.data.text)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.set_colours(Colour(255,0,0), self.data.text_colour)
        self.show()

class SectorCell(FixedSizeLabel):
    # cell displaying info on each sector

    def __init__(self, height:int, data:SectorCellData):
        super().__init__(data.width, height)
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