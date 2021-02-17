
from typing import NamedTuple
from models.dicts import SectorDict, ColourDict, GradeDict
from APImodels.sector import Sector
from APImodels.colour import Colour

class SectorCellData(NamedTuple):
    # cell model containing data for sector cell

    col   : int
    width : int
    bg_colour : Colour
    text_colour : Colour
    text : str
    problem_count : str

class SectorCellDataBuilder():
    # build sector cell data from either:
    #  - sectors
    #  - col - in case there isn't one

    def __init__(self, sector_setting: SectorDict, colour_setting:ColourDict):
        self.sector_setting = sector_setting
        self.colour_setting = colour_setting

    def from_sector(self, sector:Sector):

        col   = self.sector_setting.get_col(sector.name)
        width = 96 
        text  = sector.name.upper()
        count = str(sector.count)
        bg_colour   = self._extract_background_colour(sector.setting)
        text_colour = self._extract_text_colour(sector.setting)
    
        return SectorCellData(col, width, bg_colour, text_colour, text, count)

    def _extract_background_colour(self, setting:bool):
        R,G,B = self.colour_setting.get_colour('default')[0:3]
        if setting:
            R,G,B =  self.colour_setting.get_colour('setting')[0:3]
        return Colour(R,G,B)

    def _extract_text_colour(self, setting:bool):
        R,G,B = self.colour_setting.get_colour('default')[3:6]
        if setting:
            R,G,B =  self.colour_setting.get_colour('setting')[3:6]
        return Colour(R,G,B)
    
    def from_col(self, col:int):
        width        = 96 
        text         = self.sector_setting.get_sector(col).upper()
        bg_colour    = self._extract_background_colour(False)
        text_colour  = self._extract_text_colour(False)

        return SectorCellData(col, width, bg_colour, text_colour, text, '0') 


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

    def __init__(self, grade_setting: GradeDict, colour_setting: ColourDict):
        self.grade_setting  = grade_setting
        self.colour_setting = colour_setting

    def build(self, row:int):
        
        width = 160
        height = 48
        inner_width = 52
        inner_height = 23
        bg_colour   = self.__extract_background_colour(row)
        text_colour = self.__extract_text_colour(row)
        aim         = str(self.grade_setting.get_aim(row))
        return GradeCellData(row, width, height, inner_width, inner_height, bg_colour, text_colour, aim)

    def __extract_background_colour(self, row:int):
        grade_str = self.grade_setting.get_grade(row)
        R,G,B = self.colour_setting.get_colour(grade_str)[0:3]
        return Colour(R,G,B)

    def __extract_text_colour(self, row:int):
        grade_str = self.grade_setting.get_grade(row)
        R,G,B = self.colour_setting.get_colour(grade_str)[3:6]
        return Colour(R,G,B)
    


class GradeCountData(NamedTuple):
    # data for cell that counts problems of that particular grade

    row :int
    width : int 
    height : int
    bg_colour: Colour
    text_colour: Colour
    text : str

class GradeCountDataBuilder():
    # build grade count data from :
    #  - row + count

    def __init__(self, grade_setting: GradeDict, colour_setting: ColourDict):
        self._grade_setting  = grade_setting
        self._colour_setting = colour_setting

    def build(self, row:int, count:int):
        
        width  = 50
        height = 48
        bg_colour   = self._extract_background_colour(row, count)
        text_colour = self._extract_text_colour(row, count)

        return GradeCountData(row, width, height, bg_colour, text_colour, str(count))

    def _extract_background_colour(self, row:int, count:int):
        # return background colour depending on whether or not number of problems in that
        # grade meets the target
        aim = self._grade_setting.get_aim(row)

        if count < aim:
            R,G,B = self._colour_setting.get_colour('alert')[0:3]
        else:
            R,G,B = self._colour_setting.get_colour('default')[0:3]
        return Colour(R,G,B)

    def _extract_text_colour(self, row:int, count:int):
        # return tex colour depending on whether or not number of problems in that
        # grade meets the target
        aim = self._grade_setting.get_aim(row)

        if count < aim:
            R,G,B = self._colour_setting.get_colour('alert')[3:6]
        else:
            R,G,B = self._colour_setting.get_colour('default')[3:6]
        return Colour(R,G,B)   