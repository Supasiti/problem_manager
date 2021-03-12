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
        raise ValueError('The sector name does not exist!: {}'.format(name))
    
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
        # requirement:
        #  - one to one maping between sector and col 
        #  - col must be unique from 0,1, ..., n
        #  - if any of these conditions fails - raise
        data_copy = self._data.copy()
        if not self._update_sector_dict(value, data_copy): return True
        if self._columns_is_not_range(data_copy):
            raise ValueError('Cannot update grade setting: the list of rows must start from 0,1,2, ... to n.')
        self._data = data_copy
        return True
    
    def _update_sector_dict(self, value: SectorStyle, data:dict) -> bool:
        # return False if it didn't update the dictionary
        if isinstance(value, SectorStyle):
            self._update_if_is_SectorStyle(value, data)
        elif isinstance(value, tuple):
            for style in value:
                self._update_if_is_SectorStyle(style, data)
        else: 
            return False
        return True
    
    def _update_if_is_SectorStyle(self, value: SectorStyle, data:dict):
        if isinstance(value, SectorStyle):
            self._remove_duplicates(value, data)
            data[value.name] = value.col
    
    def _remove_duplicates(self, style:SectorStyle, data:dict):
        duplicates = [r  for r,s in data.items() if int(s) == style.col]
        for name in duplicates:
            data.pop(name)
    
    def _columns_is_not_range(self, data:dict) -> bool:
        return not all( int(c) >= 0 and int(c) < len(data) for c in data.values())