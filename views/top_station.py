# top work station with 
#  - Date
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

from views.frame import FixedHeightFrame

class TopStation(FixedHeightFrame):

    def __init__(self, controller, model):
        self.controller = controller   
        self.model      = model
        super().__init__(model.static_data.height)

        self.__init_static_UI()
        self.__connect_model()
    
    def __init_static_UI(self):
        data  = self.model.static_data
        self.date_label = QLabel(data.label_text)
        self.date_label.setFixedWidth(data.label_width)
        self.date_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        
        self.date_lineedit = QLineEdit(self.model.date_str)
        self.__set_layout()

    def __set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_lineedit)
        self.setLayout(layout)

    def __connect_model(self):
        self.model.dataChanged.connect(self.date_lineedit.setText)