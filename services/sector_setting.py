from typing import NamedTuple


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