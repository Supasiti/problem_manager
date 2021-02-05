# Main presenter
#
# contains all the informations being presented on MainView

from PyQt5.QtCore import QObject
from models.dicts import GradeDict, SectorDict
from models.problem_scroll_area_model import ProblemScrollAreaModel
from models.bottom_model import BottomStationModel

class MainModel(QObject):
    # store all the information on the view
    
    def __init__(self):
        super().__init__()
        self.grade_setting  = GradeDict()
        self.sector_setting = SectorDict()
        self.problem_scroll_area_model = ProblemScrollAreaModel(self.grade_setting, self.sector_setting)
        self.bottom_model = BottomStationModel()

        