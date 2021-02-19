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

    def to_dict(self) -> dict:
        result = {
            'grade'     : self.grade._asdict(),
            'row'       : self.row,
            'aim'       : self.aim,
            'bg_colour'    : self.bg_colour._asdict(),
            'text_colour'  : self.text_colour._asdict(),
            'hover_colour' : self.hover_colour._asdict()
        }
        return result 


class GradeStyleBuilder():

    def from_json(self, data:dict) -> GradeStyle:
        grade = Grade.from_json(data['grade'])
        row   = int(data['row'])
        aim   = int(data['aim'])
        bg_colour = Colour.from_json(data['bg_colour'])
        text_colour = Colour.from_json(data['text_colour'])
        hover_colour = Colour.from_json(data['hover_colour'])

        return GradeStyle(grade, row, aim, bg_colour, text_colour, hover_colour)


class GradeSetting():

    def __init__(self, data:tuple[GradeStyle,...]):
        self._data = data
    
    def get_row(self, grade: Grade) -> int:
        result = list([style.row for style in self._data if style.grade == grade])
        if len(result) > 0:
            return result[0]
        raise IndexError('this grade {} doesn\'t exist.'.format(str(grade)))
    
    def get_grade(self, row:int) -> Grade:
        result = list([style.grade for style in self._data if style.row == row])
        if len(result) >0:
            return result[0]
        raise IndexError('index is out of range.')
    
    def get_all_grades(self) -> tuple[Grade,...]:
        return tuple((style.grade for style in self._data))
        
    def get_aim(self, row:int) -> int:
        result = list([style.aim for style in self._data if style.row == row])
        if len(result) >0:
            return result[0]
        raise IndexError('index is out of range.')

    def get_bg_colour(self, row:int) -> Colour:
        result = list([style.bg_colour for style in self._data if style.row == row])
        if len(result) >0:
            return result[0]
        raise IndexError('index is out of range.')
    
    def get_text_colour(self, row:int) -> Colour:
        result = list([style.text_colour for style in self._data if style.row == row])
        if len(result) >0:
            return result[0]
        raise IndexError('index is out of range.')

    def length(self):
        return len(self._data)