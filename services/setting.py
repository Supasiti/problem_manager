from abc import ABC, abstractmethod
from typing import NamedTuple
from threading import Lock
import json
import os

from services.signal import Signal
from services.file_setting import FileSetting
from services.grade_setting  import GradeSetting,  GradeStyle, GradeStyleBuilder
from services.colour_setting import ColourSetting, ColourStyle
from services.sector_setting import SectorSetting, SectorStyle

class Setting():

    padlock        = Lock()
    settingChanged = Signal(type)
    
    def __init__(self):
        self._settings        = dict()
        self._init_all_setting()

    def _init_all_setting(self) -> None:
        file_parser = FileSettingParser()
        self._register(FileSetting, file_parser.get_data(), file_parser)

        grade_parser = GradeSettingParser()
        self._register(GradeSetting, grade_parser.get_data(), grade_parser)

        colour_parser = ColourSettingParser()
        self._register(ColourSetting, colour_parser.get_data(), colour_parser)
        
        sector_parser = SectorSettingParser()
        self._register(SectorSetting, sector_parser.get_data(), sector_parser)

    def get(self, class_type:type) -> object:
        if class_type in self._settings.keys():
            return self._settings[class_type].setting
        return None

    def _register(self, class_type: type, setting:object, parser:object) -> bool:
        if isinstance(setting, class_type):
            with self.padlock:
                self._settings[class_type] = SettingParserData(setting, parser)
            return True
        raise ValueError('_register(): Trying to register an incorrect setting class.')

    def update(self, class_type:type, value:object) ->bool:
        if class_type in self._settings.keys():
            parser = self._settings[class_type].parser
            parser.set_data(value)
            self._register(class_type, parser.get_data(), parser)
            self.settingChanged.emit(class_type)
            return True
        raise ValueError('This setting has not been registered.')

    def write(self, class_type:type):
        if class_type in self._settings.keys():
            parser = self._settings[class_type].parser
            parser.write()


class SettingParser(ABC):
    # based setting parser to read/write configuration on loading / change

    def load_config(self, filepath:str) -> object:
        with open(filepath, 'r') as fid:
            raw_data = json.loads(fid.read())
            fid.close()
        return raw_data
    
    def write(self, filepath:str, data:object) -> None:
        with open(filepath, 'w' ) as fid:
            json.dump(data, fid, indent=4, sort_keys=True)
            fid.truncate()
            fid.close()

    @abstractmethod
    def set_filepath(self, filepath:str) -> None:
        pass

    @abstractmethod
    def get_data(self) -> object:
        pass
    
    @abstractmethod
    def set_data(self, value:object) ->bool:
        pass


class FileSettingParser(SettingParser):
    # read/write file paths on loading / change
    # filepath of config.json file is expected to be in the folder: /config

    def __init__(self):
        self._filepath = self._create_filepath()
        self._data     = self.load_config(self._filepath)
    
    def _create_filepath(self):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, 'config','config.json')

    def write(self) -> None:
        SettingParser.write(self, self._filepath, self._data)

    def set_filepath(self, filepath:str) -> None:
        self._filepath = filepath
        self._data     = self.load_config(self._filepath)

    def get_data(self) -> object:
        return FileSetting(self._data['content path'])
    
    def set_data(self, value:object) ->bool:
        self._data['content path'] = value
        return True


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


class SettingParserData(NamedTuple):
    setting : object
    parser  : SettingParser
