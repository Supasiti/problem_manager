# template for fixed size/width/height label

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

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

    def __init__(self, width:int, height:int, name:str):
        super().__init__(width, height)
        self.name = name
        self.set_background_colour(30,30,30)
