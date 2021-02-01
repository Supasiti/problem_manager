# template for fixed size/width/height frame

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QSizePolicy

class Frame(QLabel):

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Panel)   
        self.setLineWidth(1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 

class FixedSizeFrame(Frame):

    def __init__(self, width, height):
        super().__init__()
        self.setFixedWidth(width) 
        self.setFixedHeight(height) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 

class FixedHeightFrame(Frame):

    def __init__(self,  height):
        super().__init__()
        self.setFixedHeight(height) 
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 

class FixedWidthFrame(Frame):

    def __init__(self, width):
        super().__init__()
        self.setFixedWidth(width) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding) 