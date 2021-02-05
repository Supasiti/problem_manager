
from typing import NamedTuple
from models.dicts import SectorDict, ColourDict
from APImodels.sector import Sector
from APImodels.colour import Colour


class SectorCellModel(NamedTuple):

    col : int
    bg_colour : Colour
    text_colour : Colour
    text : str
    problem_count : str

class SectorCellModelBuilder():
    # build problem cell model from either:
    #  - sectors
    #  - col - in case there isn't one

    def __init__(self):
        self.sector_setting = SectorDict()
        self.colour_setting = ColourDict()

    def build_from_sector(self, sector:Sector):

        col = self.sector_setting.get_col(sector.name)
        text = sector.name.upper()
        count = str(sector.count)
        bg_colour   = self.__extract_background_colour(sector.setting)
        text_colour = self.__extract_text_colour(sector.setting)
    
        return SectorCellModel(col, bg_colour, text_colour, text, count)

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

        text         = self.sector_setting.get_sector(col).upper()
        bg_colour    = self.__extract_background_colour(False)
        text_colour  = self.__extract_text_colour(False)

        return SectorCellModel(col, bg_colour, text_colour, text, '0') 