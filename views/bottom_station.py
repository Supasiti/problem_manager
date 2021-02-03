# bottom work station with 
#  - folder to look for data

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtCore import Qt

from views.frame import FixedHeightFrame

class BottomStation(FixedHeightFrame):

    def __init__(self):
        super().__init__(height=80)
        
        self.path_label = self.create_path_label()
        self.path_lineedit = QLabel('path here')
        self.change_button = self.create_change_button()
        self.set_layout()

    def create_path_label(self):
        path_label = QLabel('Content Path:')
        path_label.setFixedWidth(100)
        path_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        return path_label

    def create_change_button(self):
        button = QPushButton('Change')
        button.setFixedWidth(100)
        return button
    
    def set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_lineedit)
        layout.addWidget(self.change_button)
        self.setLayout(layout)
