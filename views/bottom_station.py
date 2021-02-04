# bottom work station with 
#  - folder to look for data

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtCore import Qt

from views.frame import FixedHeightFrame

class BottomStation(FixedHeightFrame):

    def __init__(self, controller, model):
        super().__init__(height=80)
        self.controller    = controller
        self.model         = model
        self.path_label    = self.__create_path_label()
        self.path_info     = QLabel(self.model.content_path)
        self.change_button = self.__create_change_button()
        self.__set_layout()

    def __create_path_label(self):
        path_label = QLabel('Content Path:')
        path_label.setFixedWidth(100)
        path_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        return path_label

    def __create_change_button(self):
        button = QPushButton('Change')
        button.setFixedWidth(100)
        return button
    
    def __set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_info)
        layout.addWidget(self.change_button)
        self.setLayout(layout)
