# top work station with 
#  - Date
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit

from PyQt5.QtCore import Qt

from views.frame import FixedHeightFrame

class TopStation(FixedHeightFrame):

    def __init__(self, controller):
        super().__init__(height=40)
        self.controller = controller

        self.date_label = self.__create_label()
        self.date_lineedit = QLineEdit('date here')
        self.__set_layout()
        
    def __create_label(self):
        label = QLabel('Date')
        label.setFixedWidth(60)
        label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        return label
    
    def __set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_lineedit)
        self.setLayout(layout)