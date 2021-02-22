from typing import NamedTuple
import os

from services.setting_parser import SettingParser

class SectorStyle(NamedTuple):

    name : str
    col   : int

    @staticmethod
    def from_json(data:dict):
        name   = data['name']
        col    = int(data['col'])

        return SectorStyle(name, col)

class SectorSetting():

    def __init__(self, data:dict[SectorStyle,...]):
        self._data = data

    def get_col(self, name: str):
        if name.lower() in self._data.keys():
            return self._data[name]
        raise ValueError('The sector name does not exist!')
    
    def get_sector(self, col:int):
        keys   = list(self._data.keys())
        values = list(self._data.values())
        if col in values:
            return keys[values.index(col)]
        raise IndexError('index is out of range.')

    def get_all_sectors(self): 
        return tuple(self._data.keys())
        
    def length(self):
        return len(self._data)


class SectorSettingParser(SettingParser):
    # read/write setting on sector 
    # filepath of sectors.json  is expected to be iin the folder: /config

    def __init__(self):
        self._filepath = self._create_filepath()
        self._data     = self.load_config(self._filepath)
    
    def _create_filepath(self):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, 'config','sectors.json')

    def write(self):
        SettingParser.write(self, self._filepath, self._data)

    def set_filepath(self, filepath:str) -> None:
        self._filepath = filepath
        self._data     = self.load_config(self._filepath)

    def get_data(self) -> object:
        return SectorSetting(dict(self._data))

    def set_data(self, value:object) -> bool:
        if isinstance(value, SectorStyle):
            self._data[value.name] = value.col
        if isinstance(value, tuple):
            for style in value:
                self._data[style.name] = style.col
        return True