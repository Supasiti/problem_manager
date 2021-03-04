from typing import NamedTuple

from services.setting import Setting
from services.grade_setting import GradeSetting
from services.colour_setting import ColourSetting
from APImodels.colour import Colour

class GradeCellData(NamedTuple):
    # model for grade cell

    row : int
    width : int
    height : int
    inner_width : int
    inner_height :int
    bg_colour : Colour
    text_colour : Colour
    aim : str

class GradeCellDataBuilder():
    # build grade cell model from either:
    #  - row 

    def __init__(self, grade_setting: GradeSetting):
        self.grade_setting  = Setting.get(GradeSetting)

    def build(self, row:int):
        width  = 160
        height = 48
        inner_width  = 52
        inner_height = 23
        bg_colour    = self.grade_setting.get_bg_colour(row)
        text_colour  = self.grade_setting.get_text_colour(row)
        aim          = str(self.grade_setting.get_aim(row))

        return GradeCellData(row, width, height, inner_width, inner_height, bg_colour, text_colour, aim)



class GradeCountData(NamedTuple):
    # data for cell that counts problems of that particular grade

    row :int
    bg_colour: Colour
    text_colour: Colour
    text : str

class GradeCountDataBuilder():
    # build grade count data from :
    #  - row + count

    def __init__(self, grade_setting: GradeSetting, colour_setting: ColourSetting):
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