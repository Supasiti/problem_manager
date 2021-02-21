from typing import NamedTuple
import os

from APImodels.colour import Colour
from APImodels.grade import Grade
from services.setting_parser import SettingParser

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

    def get_hold_colours(self, grade: Grade):
        if str(grade) in self._data.keys():
            return (str(grade).split(' ')[0], 'orange')

    def get_bg_colour(self, name:str):
        if name.lower() in self._data.keys():
            return self._data[name].bg_colour
        raise ValueError('Invalid colour name')

    def get_text_colour(self, name:str):
        if name.lower() in self._data.keys():
            return self._data[name].text_colour
        raise ValueError('Invalid colour name')

    def get_hover_colour(self, name:str):
        if name.lower() in self._data.keys():
            return self._data[name].hover_colour
        raise ValueError('Invalid colour name')


class ColourSettingParser(SettingParser):
    # read/write setting on colour scheme
    # filepath of colours.json  is expected to be iin the folder: /config

    def __init__(self):
        self._filepath = self._create_filepath()
        self._data     = self.load_config(self._filepath)
    
    def _create_filepath(self):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, 'config','colours.json')

    def write(self):
        SettingParser.write(self, self._filepath, self._data)
    
    def set_filepath(self, filepath:str) -> None:
        self._filepath = filepath
        self._data     = self.load_config(self._filepath)

    def get_data(self) -> object:
        styles = { name : ColourStyle.from_json(style) for name,style in self._data.items()}
        return ColourSetting(dict(styles))
    
    def set_data(self, value:object) ->bool:
        if isinstance(value, ColourStyle):
            self._data[value.name] = value.to_dict()
        if isinstance(value, tuple):
            for style in value:
                self._data[style.name] = style.to_dict()
        return True