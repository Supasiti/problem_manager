# main work station with the overview of the current problems in the gym

from PyQt5.QtWidgets import QGridLayout

from views.frame import Frame
from views.scroll_area import ProblemScrollArea, FixedHeightScrollArea, FixedWidthScrollArea
from views.label import FixedSizeLabel

class WorkStation(Frame):

    def __init__(self):
        super().__init__()
        
        self.info         = FixedSizeLabel(160, 48)
        self.sector_view  = FixedHeightScrollArea(48)
        self.grade_view   = FixedWidthScrollArea(160)
        self.problem_view = ProblemScrollArea()
        self.config_layout()
        
    def config_layout(self):
        grid = QGridLayout()
        grid.setContentsMargins(2,2,2,2)
        grid.setSpacing(4)
        grid.addWidget(self.info,         0, 0)
        grid.addWidget(self.sector_view,  0, 1)
        grid.addWidget(self.grade_view,   1, 0)
        grid.addWidget(self.problem_view, 1, 1)
        self.setLayout(grid)

    