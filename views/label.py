# template for fixed size/width/height label

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

class FixedSizeLabel(QLabel):

    def __init__(self, width:int, height:int):
        super().__init__()
        self.setFixedWidth(width) 
        self.setFixedHeight(height) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 
        self.set_background_colour(20,20,20)

    def set_background_colour(self, R, G, B):
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(R, G, B))
        self.setPalette(pal)


class ProblemCell(FixedSizeLabel):
    # cell displaying info on problem if there is

    def __init__(self, width:int, height:int, row:int, col:int):
        super().__init__(width, height)
        self.row = row
        self.col = col
        self.clicked_command = None
        
        self.set_background_colour(30,30,30)
        self.__add_mouse_effect()

    def __add_mouse_effect(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.enterEvent  = self.__add_hover_effect
        self.leaveEvent  = self.__remove_hover_effect

        if not self.clicked_command is None:
            self.mousePressEvent = self.on_mouse_clicked
    
    def on_mouse_clicked(self, event):
        if not self.clicked_command is None:
            self.clicked_command(self.row, self.col)
    
    def __add_hover_effect(self, event):
        self.set_background_colour(60,60,60)
    
    def __remove_hover_effect(self, event):
        self.set_background_colour(30,30,30)

    def set_clicked_command(self, command):
        self.clicked_command = command
        self.mousePressEvent = self.on_mouse_clicked

class GradeCell(FixedSizeLabel):
    # cell displaying info related to the grade

    def __init__(self, width:int, height:int, name:str):
        super().__init__(width, height)
        self.name = name
        self.set_background_colour(30,30,30)

class SectorCell(FixedSizeLabel):
    # cell displaying info on each sector

     def __init__(self, width:int, height:int, name:str):
        super().__init__(width, height)
        self.name = name
        self.set_background_colour(30,30,30)