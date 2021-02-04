from PyQt5.QtCore import QObject
from presenters.dicts import GradeDict, SectorDict

class ProblemScrollAreaPresenter(QObject):

    def __init__(self, grade_setting: GradeDict, sector_setting: SectorDict):
        super().__init__()
        self.grade_setting = grade_setting
        self.sector_setting = sector_setting

        