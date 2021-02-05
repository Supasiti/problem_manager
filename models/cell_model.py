
from collections import namedtuple
from models.dicts import SectorDict

class SectorCellModel(
    namedtuple('SectorCellModel',
        ['col','bg_colour', 'text_colour', 'text', 'problem_count']
    )):
    
    @staticmethod
    def from_sector(sector):
        pass


