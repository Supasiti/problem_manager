from typing import NamedTuple
from services.setting import Setting
from services.grade_setting import GradeSetting
from services.colour_setting import ColourSetting
from services.sector_setting import SectorSetting
from APImodels.problem import Problem 
from APImodels.colour import Colour

class ProblemCellData(NamedTuple):

    row : int
    col : int
    bg_colour : Colour
    text_colour : Colour
    hover_colour : Colour
    text : str
    RIC : str
    id : int

class ProblemCellDataBuilder():
    # build problem cell model from either:se
    #  - problem
    #  - row, col - in case there isn't one

    def __init__(self):
        self._grade_setting  = Setting.get(GradeSetting)
        self._colour_setting = Setting.get(ColourSetting)
        self._sector_setting = Setting.get(SectorSetting)

    def from_problem(self, problem:Problem):

        hold_colour  = self._extract_hold_colour(problem)

        row          = self._grade_setting.get_row(problem.grade)
        col          = self._sector_setting.get_col(problem.sector)
        bg_colour    = self._colour_setting.get_bg_colour(hold_colour)
        text_colour  = self._colour_setting.get_text_colour(hold_colour)
        hover_colour = self._colour_setting.get_hover_colour(hold_colour)
        text         = problem.styles[0]
        RIC          = str(problem.RIC)
        problem_id   = problem.id

        return ProblemCellData(row, col, bg_colour, text_colour, hover_colour,
            text, RIC, problem_id)
        
    def _extract_hold_colour(self, problem: Problem):
        return str(problem.grade) if problem.colour == problem.grade.range else problem.colour
        
    def empty_cell(self, row:int, col:int):

        bg_colour    = self._colour_setting.get_bg_colour('default')
        text_colour  = self._colour_setting.get_text_colour('default')
        hover_colour = self._colour_setting.get_hover_colour('default')

        return ProblemCellData(row, col, bg_colour, text_colour, hover_colour,
            '', '', 0)