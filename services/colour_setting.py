from typing import NamedTuple

from APImodels.colour import Colour
from APImodels.grade import Grade

class ColourStyle(NamedTuple):

    name      : str
    bg_colour : Colour
    text_colour : Colour
    hover_colour : Colour

    def to_dict(self) -> dict:
        result = {
            'name'         : self.name,
            'bg_colour'    : self.bg_colour._asdict(),
            'text_colour'  : self.text_colour._asdict(),
            'hover_colour' : self.hover_colour._asdict()
        }
        return result 
        
    @staticmethod
    def from_json(data:dict):
        name         = data['name']
        bg_colour    = Colour.from_json(data['bg_colour'])
        text_colour  = Colour.from_json(data['text_colour'])
        hover_colour = Colour.from_json(data['hover_colour'])

        return ColourStyle(name, bg_colour, text_colour, hover_colour)

class ColourSetting():

    def __init__(self, data:dict):
        self._data = data

    def get_colour(self, name: str) -> ColourStyle:
        if name.lower() in self._data.keys():
            return self._data[name]
        raise ValueError('Invalid colour name')
    
    def get_grade_colour(self, grade: Grade)-> ColourStyle:
        if str(grade) in self._data.keys():
            return self._data[str(grade)]
        raise ValueError('Invalid colour name')

    def get_hold_colours(self, name: str):
        if name.lower() in self._data.keys():
            return (name.split(' ')[0], 'orange')

    def get_bg_colour(self, name:str):
        if name.lower() in self._data.keys():
            return self._data[name].bg_colour
        raise ValueError('Invalid colour name')

    def get_text_colour(self, name:str):
        if name.lower() in self._data.keys():
            return self._data[name].text_colour
        raise ValueError('Invalid colour name')