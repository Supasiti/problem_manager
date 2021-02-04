# global main window

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout

from controllers.main_controller import MainController 
from models.main_model import MainModel

from views.work_station import WorkStation
from views.top_station import TopStation
from views.bottom_station import BottomStation
from views.tool_station import ToolStation

class MainView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.model = MainModel()
        self.controller = MainController(self.model)   
        
        self.top_station = TopStation(self.controller)
        self.work_station = WorkStation(self.controller, self.model)
        self.tool_station = ToolStation(self.controller)
        self.bottom_station = BottomStation(self.controller, self.model.bottom_model)

        self.__init_UI()
        
    def __init_UI(self):
        self.title = 'Problem Manager'
        self.setWindowTitle(self.title)  
        
        self.width  = 1200
        self.height =  800
        self.setMinimumSize(self.width, self.height) 

        self.__init_window_area()
        
    def __init_window_area(self):
        
        window_area = QLabel() 
        window_layout = QGridLayout()
        window_layout.setSpacing(4)

        window_layout.addWidget(self.top_station,    0, 0)
        window_layout.addWidget(self.work_station,   1, 0)
        window_layout.addWidget(self.bottom_station, 2, 0)
        window_layout.addWidget(self.tool_station,   0, 1, 3, 1) 
        
        window_area.setLayout(window_layout)
        self.setCentralWidget(window_area)  
