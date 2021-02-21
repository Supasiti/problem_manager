from typing import NamedTuple
import os

from APImodels.colour import Colour
from APImodels.grade import Grade
from services.setting_parser import SettingParser

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
    # assume that there is one-to-one mapping between grades and rows
    # rows is 0,1,2,.. , n
    
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


class GradeSettingParser(SettingParser):
    # read/write setting on gradings
    # filepath of grades.json is expected to be in the folder: /config
    # data : str(row) : GradeStyle
    #   - one to one maping between row and grade name
    #   - row must be unique from 0,1,2 ...

    def __init__(self):
        self._filepath = self._create_filepath()
        self._data     = self.load_config(self._filepath)
    
    def _create_filepath(self):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, 'config','grades.json')

    def write(self):
        SettingParser.write(self, self._filepath, self._data)

    def set_filepath(self, filepath:str) -> None:
        self._filepath = filepath
        self._data     = self.load_config(self._filepath)

    def get_data(self) -> object:
        builder = GradeStyleBuilder()
        styles = [builder.from_json(style) for style in self._data.values()]
        return GradeSetting(tuple(styles))
    
    def set_data(self, value:object) ->bool:
        # requirement:
        #  - one to one maping between row and grade name
        #  - row must be unique from 0,1,2 ...
        #  - if any of these conditions fails - raise
        data_copy = self._data.copy()
        if not self._update_grade_dict(value, data_copy): return True
        if self._keys_is_not_range(data_copy):
            raise ValueError('Cannot update grade setting: the list of rows must start from 0,1,2, ... to n.')
        self._data = data_copy
        return True

    def _keys_is_not_range(self, data:dict) -> bool:
        return not all( int(r) >= 0 and int(r) < len(data) for r in data.keys())

    def _update_grade_dict(self, value: GradeStyle, data:dict) -> bool:
        # return False if it didn't update the dictionary
        if isinstance(value, GradeStyle):
            self._update_if_is_GradeStyle(value, data)
        elif isinstance(value, tuple):
            for style in value:
                self._update_if_is_GradeStyle(style, data)
        else: 
            return False
        return True

    def _update_if_is_GradeStyle(self, value: GradeStyle, data:dict):
        if isinstance(value, GradeStyle):
            self._remove_duplicates(value, data)
            data[str(value.row)] = value.to_dict()

    def _remove_duplicates(self, style:GradeStyle, data:dict):
        duplicates = [r  for r,s in data.items() if s['grade'] == style.grade._asdict()]
        for row in duplicates:
            data.pop(str(row))