from typing import NamedTuple

from models.dicts import GradeDict, ColourDict, SectorDict
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

    def __init__(self, 
        grade_setting : GradeDict, 
        colour_setting: ColourDict, 
        sector_setting: SectorDict):
        self.grade_setting  = grade_setting
        self.colour_setting = colour_setting
        self.sector_setting = sector_setting

    def build_from_problem(self, problem:Problem):
        
        grade_str   = self.__extract_grade(problem)
        hold_colour = self.__extract_hold_colour(problem)

        row          = self.grade_setting.get_row(grade_str)
        col          = self.sector_setting.get_col(problem.sector)
        bg_colour    = self.__extract_background_colour(hold_colour)
        text_colour  = self.__extract_text_colour(hold_colour)
        hover_colour = self.__extract_hover_colour(hold_colour)
        text         = problem.styles[0]
        RIC          = str(problem.RIC)
        problem_id   = problem.id

        return ProblemCellData(row, col, bg_colour, text_colour, hover_colour,
            text, RIC, problem_id)

    def __extract_grade(self, problem: Problem):
        return str(problem.grade)
        
    def __extract_hold_colour(self, problem: Problem):
        if problem.colour == problem.grade.range:
            return str(problem.grade)
        else:
            return problem.colour

    def __extract_background_colour(self, hold_colour=None):
        R,G,B = self.colour_setting.get_colours('default')[0:3]
        if not hold_colour is None:
            R,G,B =  self.colour_setting.get_colours(hold_colour)[0:3]
        return Colour(R,G,B)
       
    def __extract_text_colour(self, hold_colour=None):
        R,G,B =  self.colour_setting.get_colours('default')[3:6]
        if not hold_colour is None:
            R,G,B =  self.colour_setting.get_colours(hold_colour)[3:6]
        return Colour(R,G,B)
    
    def __extract_hover_colour(self, hold_colour=None):
        R,G,B = self.colour_setting.get_colours('default')[6:9]
        if not hold_colour is None:
            R,G,B =  self.colour_setting.get_colours(hold_colour)[6:9]
        return Colour(R,G,B)
        

    def empty_cell(self, row:int, col:int):

        bg_colour    = self.__extract_background_colour()
        text_colour  = self.__extract_text_colour()
        hover_colour = self.__extract_hover_colour()

        return ProblemCellData(row, col, bg_colour, text_colour, hover_colour,
            '', '', 0)