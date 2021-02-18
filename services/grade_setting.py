from typing import NamedTuple

from APImodels.colour import Colour
from APImodels.grade import Grade

class GradeStyle(NamedTuple):

    grade : Grade
    row   : int
    aim   : int
    bg_colour : Colour
    text_colour : Colour
    hover_colour : Colour

class GradeSetting():

    def __init__(self, data:tuple):
        self._data = data
    
     def get_row(self, grade: Grade) -> int:
        result = list([style.grade for style in self._data if style.row == row])
        
    
    def get_grade(self, row:int) -> Grade:
        result = list([style.grade for style in self._data if style.row == row])
        if len(result) >0:
            return result[0]
        raise IndexError('index is out of range.')
    
    def get_all_grades(self) -> tuple[Grade,...]:
        return tuple(self._data.keys())
        
    def get_aim(self, row:int) -> int:
        values = list(self._grade_dict.values())
        rows   = [value[0] for value in values]
        aims   = [value[1] for value in values]
        if row in rows:
            return aims[rows.index(row)]
        raise IndexError('index is out of range.')

    def length(self):
        return len(self._grade_dict)