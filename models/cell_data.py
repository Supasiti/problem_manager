
from typing import NamedTuple
from models.dicts import SectorDict, ColourDict
from APImodels.sector import Sector
from APImodels.colour import Colour
from APImodels.grade import GradeCount

class SectorCellData(NamedTuple):
    # cell model containing data for sector cell

    col   : int
    width : int
    bg_colour : Colour
    text_colour : Colour
    text : str
    problem_count : str

class SectorCellDataBuilder():
    # build sector cell model from either:
    #  - sectors
    #  - col - in case there isn't one

    def __init__(self, sector_setting: SectorDict, colour_setting:ColourDict):
        self.sector_setting = sector_setting
        self.colour_setting = colour_setting
        self.max_col = self.sector_setting.length()

    def build_from_sector(self, sector:Sector):

        col   = self.sector_setting.get_col(sector.name)
        width = 96 if col < self.max_col - 1  else 110
        text  = sector.name.upper()
        count = str(sector.count)
        bg_colour   = self.__extract_background_colour(sector.setting)
        text_colour = self.__extract_text_colour(sector.setting)
    
        return SectorCellData(col, width, bg_colour, text_colour, text, count)

    def __extract_background_colour(self, setting:bool):
        R,G,B = self.colour_setting.get_colours('default')[0:3]
        if setting:
            R,G,B =  self.colour_setting.get_colours('setting')[0:3]
        return Colour(R,G,B)

    def __extract_text_colour(self, setting:bool):
        R,G,B = self.colour_setting.get_colours('default')[3:6]
        if setting:
            R,G,B =  self.colour_setting.get_colours('setting')[3:6]
        return Colour(R,G,B)
    
    def build_from_col(self, col:int):
        width        = 96 if col < self.max_col - 1  else 110
        text         = self.sector_setting.get_sector(col).upper()
        bg_colour    = self.__extract_background_colour(False)
        text_colour  = self.__extract_text_colour(False)

        return SectorCellData(col, width, bg_colour, text_colour, text, '0') 


class GradeCellData(NamedTuple):
    # model for grade cell

    row : int
    bg_colour : Colour
    text_colour : Colour
    count_bg_colour: Colour
    count_text_colour: Colour
    aim : str
    problem_count : str

class GradeCellDataBuilder():
    # build grade cell model from either:
    #  - grade count

    pass
