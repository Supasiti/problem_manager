# global main window
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from APImodels.colour import Colour 
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
        
        self._init_UI()
        self._populate_all_stations()
        self._connect_model()
        self._init_menu_bars()
        

    def _init_UI(self):
        data        = self.model.static_data
        self.title  = data.title
        self.width  = data.width
        self.height = data.height
        self.setWindowTitle(self.title)  
        self.setMinimumSize(self.width, self.height) 
        
        self.window = QLabel()
        self.setCentralWidget(self.window) 
        self.set_colours(Colour(45,45,45),Colour(240,240,240))
        self.layout = QGridLayout()
        self.layout.setSpacing(4)    
        self.window.setLayout(self.layout)

    def _populate_all_stations(self):
        data        = self.model.dynamic_data

        self.top_station    = data.top_station
        self.work_station   = data.work_station
        self.tool_station   = data.tool_station 
        self.bottom_station = data.bottom_station 

        self.layout.addWidget(self.top_station,    0, 1)
        self.layout.addWidget(self.work_station,   0, 0, 2, 1)
        self.layout.addWidget(self.bottom_station, 2, 0)
        self.layout.addWidget(self.tool_station,   1, 1, 2, 1)

    def _connect_model(self):
        self.model.dataChanged.connect(self._update_UI)

    def _update_UI(self):
        self._remove_all_widgets_from_layout()
        self._populate_all_stations() 
      
    def _remove_all_widgets_from_layout(self):
        self.layout.removeWidget(self.top_station)
        self.layout.removeWidget(self.work_station)
        self.layout.removeWidget(self.bottom_station)
        self.layout.removeWidget(self.tool_station)

    def _init_menu_bars(self):
        action_open_previous = MenuAction(
            'Open Set', 'Ctrl+Shift+O', 'Open to view previous set', 
            self.controller.open_previous_set, parent=self)
        action_open_current = MenuAction(
            'Open Current Set', 'Ctrl+O', 'Open the last set', 
            self.controller.open_current_set, parent=self)
        action_open_viewer = MenuAction(
            'Open Problem Viewer', 'Ctrl+Alt+O', 'Open the problem viewer', 
            self.controller.open_problem_list_viewer, parent=self)
        action_exit = MenuAction(
            'Close', 'Ctrl+Shift+X', 'Close window', 
            qApp.quit, parent=self)
        action_save = MenuAction(
            '&Save', 'Ctrl+S', 'Save current set', 
            self.controller.show_save_dialog, parent=self)
        action_save_as = MenuAction(
            '&Save as', 'Ctrl+Shift+S', 'Save as new set', 
            self.controller.show_save_as_dialog, parent=self)

        self.statusBar()
        menuBar    = self.menuBar()
        fileMenu   = menuBar.addMenu('&File')
        fileMenu.addAction(action_open_previous)
        fileMenu.addAction(action_open_current)
        fileMenu.addAction(action_open_viewer)
        fileMenu.addSeparator()
        fileMenu.addAction(action_save)
        fileMenu.addAction(action_save_as)
        fileMenu.addSeparator()
        fileMenu.addAction(action_exit)

    def set_colours(self, colour: Colour, text_colour:Colour):
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)

class MenuAction(QAction): 
    
    def __init__(self, display, shortcut, statusTip, connect=None, parent=None):
        super().__init__(display, parent=parent)
        
        self.setShortcut(shortcut)
        self.setStatusTip(statusTip)
        if not connect is None:
            self.triggered.connect(connect)