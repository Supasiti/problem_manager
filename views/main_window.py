# global main window

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout

from views.work_station import WorkStation
from views.top_station import TopStation
from views.bottom_station import BottomStation
from views.tool_station import ToolStation

class MainView(QMainWindow):

    top_station : TopStation
    work_station : WorkStation
    bottom_station : BottomStation
    tool_station : ToolStation

    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller   
        self.model      = model
        
        self.__init_static_UI()
        self.__init_dynamic_UI()
        self.__connect_model()
        
    #     self.top_station = TopStation(self.controller)
    #     self.work_station = WorkStation(self.controller, self.model)
    #     self.tool_station = ToolStation(self.controller)
    #     self.bottom_station = BottomStation(self.controller, self.model.bottom_model)

    #     self.__init_UI()
        
    def __init_static_UI(self):
        data        = self.model.static_data
        self.title  = data.title
        self.width  = data.width
        self.height = data.height
        self.setWindowTitle(self.title)  
        self.setMinimumSize(self.width, self.height) 
        
        self.window = QLabel()
        self.setCentralWidget(self.window) 

    def __connect_model(self):
        self.model.dataChanged.connect(self.__init_dynamic_UI)
    
    def __init_dynamic_UI(self):
        data = self.model.dynamic_data
        self.layout = QGridLayout()
        self.layout.setSpacing(4)
        
        self.top_station    = data.top_station
        self.work_station   = data.work_station
        self.tool_station   = data.tool_station 
        self.bottom_station = data.bottom_station 
        
        

        self.layout.addWidget(self.top_station,    0, 0)
        self.layout.addWidget(self.work_station,   1, 0)
        self.layout.addWidget(self.bottom_station, 2, 0)
        self.layout.addWidget(self.tool_station,   0, 1, 3, 1) 
        
        self.window.setLayout(self.layout)

    # def __init_window_area(self):
        
    #     window_area = QLabel() 
    #     self.layout = QGridLayout()
    #     self.layout.setSpacing(4)

    #     self.layout.addWidget(self.top_station,    0, 0)
    #     self.layout.addWidget(self.work_station,   1, 0)
    #     self.layout.addWidget(self.bottom_station, 2, 0)
    #     self.layout.addWidget(self.tool_station,   0, 1, 3, 1) 
        
    #     window_area.setLayout(self.layout)
    #     self.setCentralWidget(window_area)



