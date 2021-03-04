# main work station with the overview of the current problems in the gym

from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QFont, QColor

from views.frame import Frame
from APImodels.colour import Colour

class WorkStation(Frame):

    def __init__(self, controller, model):
        super().__init__()
        self.controller   = controller
        self.model        = model

        self._init_UI()
        self._populate_main_view()


    def _init_UI(self):
        data        = self.model.static_data
        self.set_background_colour(data.bg_colour)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2,2,2,2)
        self.layout.setSpacing(4)
        self.setLayout(self.layout)
    
    def _populate_main_view(self):
        self.title = QLabel('Current Set')
        self.title.setFont(QFont('.AppleSystemUIFont', 28))
        self.title.setMargin(20)

        self.main_view = self.model.dynamic_data.main_view  
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.main_view)
    
    def update_UI(self) ->None:
        self._remove_all_widgets_from_layout()
        self._populate_main_view()

    def _remove_all_widgets_from_layout(self) -> None:
        self.layout.removeWidget(self.main_view)

    def set_background_colour(self, colour:Colour):
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        self.setAutoFillBackground(True)
        self.setPalette(pal)