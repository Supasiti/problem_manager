# main work station with the overview of the current problems in the gym

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from views.frame import Frame
from views.scroll_area import ProblemScrollArea, SectorScrollArea, GradeScrollArea
from views.label import FixedSizeLabel

class WorkStation(Frame):

    def __init__(self, controller, model):
        super().__init__()
        self.controller   = controller
        self.model        = model
        self.info         = FixedSizeLabel(160, 48)
        self.sector_view  = SectorScrollArea(self.controller, self.model.sector_scroll_area_model)
        self.grade_view   = GradeScrollArea(19)
        self.problem_view = ProblemScrollArea(self.controller, self.model.problem_scroll_area_model)
        
        self.__config_layout()
        self.set_background_colour()
        self.__connect_scroll_areas()
        
    def __config_layout(self):
        # private method to config the station layout

        grid = QGridLayout()
        grid.setContentsMargins(2,2,2,2)
        grid.setSpacing(4)
        grid.addWidget(self.info,         0, 0)
        grid.addWidget(self.sector_view,  0, 1)
        grid.addWidget(self.grade_view,   1, 0)
        grid.addWidget(self.problem_view, 1, 1)
        self.setLayout(grid)

    def set_background_colour(self):
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(45, 45, 45))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def __connect_scroll_areas(self):
        self.problem_view.connect_horizontal_scroll_bar(self.__set_horizontal_bar_value)
        self.problem_view.connect_vertical_scroll_bar(self.__set_vertical_bar_value)

    def __set_horizontal_bar_value(self, value:int):
        self.sector_view.set_horizontal_bar_value(value)

    def __set_vertical_bar_value(self, value:int):
        self.grade_view.set_vertical_bar_value(value)