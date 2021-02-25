# main work station with the overview of the current problems in the gym

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from views.label import FixedSizeLabel, InfoCell
from views.frame import Frame
from views.scroll_area import ProblemArea, SectorArea, GradeArea
from APImodels.colour import Colour

class WorkStation(Frame):

    info_view    : InfoCell
    sector_view  : SectorArea
    grade_view   : GradeArea
    problem_view : ProblemArea

    def __init__(self, controller, model):
        super().__init__()
        self.controller   = controller
        self.model        = model

        self.__init_static_UI()
        self.__init_dynamic_UI()
        self.__connect_scroll_bars()
        self.__connect_model()

    def __init_static_UI(self):
        data        = self.model.static_data
        self.top_right_pad   = FixedSizeLabel(10, 48)
        self.bottom_left_pad = FixedSizeLabel(154, 10)
        self.set_background_colour(data.bg_colour)
        
    def __init_dynamic_UI(self):
        data              = self.model.dynamic_data
        self.layout = QGridLayout()
        self.layout.setContentsMargins(2,2,2,2)
        self.layout.setSpacing(4)

        self.info_view    = InfoCell(160, 48, 52, 23, Colour(30,30,30), Colour(240,240,240))
        self.sector_view  = data.sector_view
        self.grade_view   = data.grade_view  
        self.problem_view = data.problem_view   

        self.layout.addWidget(self.info_view,      0, 0)
        self.layout.addWidget(self.sector_view,    0, 1)
        self.layout.addWidget(self.grade_view,     1, 0)
        self.layout.addWidget(self.problem_view,   1, 1, 2, 2)
        self.layout.addWidget(self.top_right_pad,  0, 2)
        self.layout.addWidget(self.bottom_left_pad,2, 0)
        self.setLayout(self.layout)

    def set_background_colour(self, colour:Colour):
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def __connect_scroll_bars(self):
        self.problem_view.connect_horizontal_scroll_bar(self.__set_horizontal_bar_value)
        self.problem_view.connect_vertical_scroll_bar(self.__set_vertical_bar_value)
        self.grade_view.connect_vertical_scroll_bar(self.__set_vertical_bar_value)

    def __set_horizontal_bar_value(self, value:int):
        self.sector_view.set_horizontal_bar_value(value)

    def __set_vertical_bar_value(self, value:int):
        self.grade_view.set_vertical_bar_value(value)
        self.problem_view.set_vertical_bar_value(value)

    def __connect_model(self):
        self.model.dataChanged.connect(self.__init_dynamic_UI)