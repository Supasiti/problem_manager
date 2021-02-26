# top work station with 
#  - Date
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

from views.frame import FixedSizeFrame

class TopStation(FixedSizeFrame):

    def __init__(self, controller, model):
        self.controller = controller   
        self.model      = model
        self.width      = self.model.static_data.width
        self.height     = self.model.static_data.height
        super().__init__(self.width, self.height)

        self._init_static_UI()
        self._connect_model()
    
    def _init_static_UI(self):
        data  = self.model.static_data
        self.date_label = QLabel(data.label_text)
        self.date_label.setFixedWidth(data.label_width)
        self.date_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        
        self.date_lineedit = QLineEdit(self.model.date_str)
        self._set_layout()

    def _set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_lineedit)
        self.setLayout(layout)

    def _connect_model(self):
        self.model.dataChanged.connect(self.date_lineedit.setText)