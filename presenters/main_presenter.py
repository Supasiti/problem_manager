# Main presenter
#
# contains all the informations being presented on MainView

from PyQt5.QtCore import QObject
from presenters.dicts import GradeDict, SectorDict
from presenters.problem_cell_model import ProblemCellModelBuidler
from models.problem import Problem
from models.grade import Grade
from models.RIC import RIC
from datetime import date
from presenters.problem_scroll_area_presenter import ProblemScrollAreaPresenter

class MainPresenter(QObject):
    # store all the information on the view
    
    def __init__(self):
        super().__init__()
        self.grade_setting  = GradeDict()
        self.sector_setting = SectorDict()
        self.problem_scroll_area_model = ProblemScrollAreaPresenter(self.grade_setting, self.sector_setting)
