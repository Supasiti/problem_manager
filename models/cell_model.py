
from collections import namedtuple

class SectorCellModel(
    namedtuple('SectorCellModel',
        ['col','bg_colour', 'text_colour', 'text', 'problem_count']
    )):
    pass

