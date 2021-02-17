from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from views.label import FixedSizeLabel, FixedWidthLabel

class FileView(FixedWidthLabel):

    def __init__(self, controller, model):
        self.controller = controller
        self.model      = model
        self.width      = self.model.static_data.width
        super().__init__(self.width)

        self._init__UI()
        self._set_data()
        self._connect_model()

    def _init__UI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(0,0,0,0)

        self.label_title = FixedSizeLabel(self.width -6, 40, 'File Viewer')
        self.label_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_title.set_colours(Colour(30,30,30), Colour(240,240,240))
 
        self.viewer = QListWidget()
        self.viewer.setFixedWidth(self.width -6)
        self.viewer.itemClicked.connect(self._item_clicked)

        self.layout.addWidget(self.label_title, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.viewer,      alignment=Qt.AlignHCenter)
        self.setLayout(self.layout)

    def _set_data(self):
        data        = self.model.view_data 
        self.viewer.clear()
        self.viewer.addItems(data.filenames)

    def _connect_model(self):
        self.model.dataChanged.connect(self._set_data)
        return True
    
    def _item_clicked(self, item):
        self.controller.on_item_clicked(item.text())