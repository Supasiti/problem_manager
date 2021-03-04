from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from typing import NamedTuple

from services.setting import Setting
from services.grade_setting import GradeSetting
from services.colour_setting import ColourSetting
from APImodels.problem import Problem
from APImodels.grade import Grade
from APImodels.colour import Colour

class GradeCellData(NamedTuple):
    # model for grade cell

    row : int   
    aim : str
    bg_colour   : Colour
    text_colour : Colour
    width   : int  = 160
    height  : int  = 48 
    inner_width  : int = 52
    inner_height : int = 23


class GradeCellDataBuilder():
    # build grade cell model from:
    #  - row 

    def __init__(self):
        self.grade_setting  = Setting.get(GradeSetting)

    def build(self, row:int):
        bg_colour    = self.grade_setting.get_bg_colour(row)
        text_colour  = self.grade_setting.get_text_colour(row)
        aim          = str(self.grade_setting.get_aim(row))

        return GradeCellData(row, aim, bg_colour, text_colour)


class GradeCountData(NamedTuple):
    # data for cell that counts problems of that particular grade

    row : int
    bg_colour: Colour
    text_colour: Colour
    text : str

class GradeCountDataBuilder():
    # build grade count data from :
    #  - row + count

    def __init__(self):
        self._grade_setting  = Setting.get(GradeSetting)
        self._colour_setting = Setting.get(ColourSetting)

    def build(self, row:int, count:int):
        bg_colour   = self._extract_background_colour(row, count)
        text_colour = self._extract_text_colour(row, count)

        return GradeCountData(row, bg_colour, text_colour, str(count))

    def _extract_background_colour(self, row:int, count:int):
        # return background colour depending on whether or not number of problems in that
        # grade meets the target
        aim        = self._grade_setting.get_aim(row)
        colour_str = 'alert' if count < aim else 'default'
        return self._colour_setting.get_bg_colour(colour_str)

    def _extract_text_colour(self, row:int, count:int):
        # return text colour depending on whether or not number of problems in that
        # grade meets the target
        aim        = self._grade_setting.get_aim(row)
        colour_str = 'alert' if count < aim else 'default'
        return self._colour_setting.get_text_colour(colour_str) 


class GradeAreaData(NamedTuple):
    cells : tuple[GradeCellData,...]
    width : int =160
    
class GradeAreaDataBuilder():

    def __init__(self):
        super().__init__()
        self.builder       = GradeCellDataBuilder()
        self.grade_setting = Setting.get(GradeSetting)
        self.n_row         = self.grade_setting.length()

    def default(self):
        cells = [self.builder.build(row) for row in range(self.n_row)]
        cells.sort(key= lambda x : x.row)
        return GradeAreaData(tuple(cells))


class GradeCountsData(NamedTuple):
    cells : tuple[GradeCountData,...]

    def get_cell(self, row:int):
        cell = [cell for cell in self.cells if cell.row == row]
        return cell[0] if len(cell) > 0 else None


class GradeCountsDataBuilder():

    def __init__(self):
        super().__init__()
        self._grade_setting  = Setting.get(GradeSetting)
        self._builder = GradeCountDataBuilder()

        self.n_row   = self._grade_setting.length()
        self._grades = self._grade_setting.get_all_grades()

    def default(self):
        cells = [self._builder.build(row, 0) for row in range(self.n_row)] 
        cells.sort(key= lambda x : x.row)
        return GradeCountsData(tuple(cells))

    def from_problems(self, problems:tuple[Problem,...]):
        prob = tuple(problems)
        if len(prob) == 0 :
            return self.default()
        cell_data = [(self._grade_setting.get_row(g), self._counts(g, prob) ) for g in self._grades]
        cells     = [self._builder.build(d[0], d[1]) for d in cell_data]
        cells.sort(key= lambda x : x.row)
        return GradeCountsData(tuple(cells))

    def _counts(self, grade:Grade, problems:tuple[Problem,...]) -> int:
        return len([p for p in problems if p.grade == grade])

class GradeAreaModel(QObject):
    
    countsChanged = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self._builder       = GradeAreaDataBuilder()
        self._count_builder = GradeCountsDataBuilder()   
        self.static  = self._builder.default()
        self._counts = self._count_builder.default()

    @property
    def counts(self) -> None:
        return self._counts

    @counts.setter
    def counts(self, value: GradeCountsData) -> None:
        self._counts = value
        self.countsChanged.emit(True)

    def update_counts(self, problems:tuple[Problem,...]) -> None:
        self.counts = self._count_builder.from_problems(problems)