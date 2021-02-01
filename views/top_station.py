# top work station with 
#  - Date
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit

from PyQt5.QtCore import Qt

from views.frame import FixedHeightFrame

class TopStation(FixedHeightFrame):

    def __init__(self):
        super().__init__(height=40)
        
        self.date_label = self.create_label()
        self.date_lineedit = QLineEdit('date here')
        self.set_layout()
        
    def create_label(self):
        label = QLabel('Date')
        label.setFixedWidth(60)
        label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        return label
    
    def set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_lineedit)
        self.setLayout(layout)