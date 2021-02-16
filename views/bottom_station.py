# bottom work station with 
#  - folder to look for data

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

from views.frame import FixedHeightFrame

class BottomStation(FixedHeightFrame):
    
    def __init__(self, controller, model):
        self.controller    = controller
        self.model         = model        
        super().__init__(self.model.static_data.height)

        self._init_UI()
        self._set_layout()
        self._connect_model()

    def _init_UI(self):
        data = self.model.static_data
        self.path_label    = QLabel(data.label_text)
        self.path_info     = QLabel(self.model.dynamic_data)
        self.change_button = QPushButton(data.button_text) 
        self._config_UI()

    def _config_UI(self):
        data = self.model.static_data
        self.path_label.setFixedWidth(data.label_width)
        self.path_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)        

        self.change_button.setFixedWidth(data.button_width)
        self.change_button.clicked.connect(self._openFileNameDialog)

    def _set_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_info)
        layout.addWidget(self.change_button)
        self.setLayout(layout)

    def _openFileNameDialog(self, event):
        # set up open file window
        
        directory = QFileDialog.getExistingDirectory(self, "Open Directory",
                    "~/Desktop", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if directory: 
            self.controller.open_directory(directory)

    def _connect_model(self):
        self.model.contentPathChanged.connect(self.path_info.setText)