from abc import ABC, abstractmethod
from typing import NamedTuple
from threading import Lock
import json
import os

from services.signal import Signal
from services.file_setting import FileSetting

class ConfigParser():
    # read/write configure file on loading / change
    # filepath of config.json file is expected to be in the same folder as this class.

    _data : dict

    def __init__(self):
        self._filepath = self._create_filepath()
        self.load_config(self._filepath)
    
    def _create_filepath(self):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, 'config.json')

    @property
    def data(self) -> dict:
        return self._data
    
    @data.setter
    def data(self, new_data:dict) -> bool:
        self._data = new_data
        # probably need to write config file here

    def load_config(self, filepath:str):
        with open(filepath, 'r') as fid:
            self._data = json.loads(fid.read())


class Setting():

    padlock        = Lock()
    settingChanged = Signal(bool)
    
    def __init__(self):
        self._parser          = ConfigParser()
        self._settings        = dict()
        self._init_all_setting()

    def _init_all_setting(self) -> None:
        file_parser = FileSettingParser(self._parser)
        self._register(FileSetting, file_parser.get_data(), file_parser)

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
            self._register(FileSetting, parser.get_data(), parser)
            self.settingChanged.emit(True)
            return True
        raise ValueError('This setting has not been registered.')


class SettingParser(ABC):

    def __init__(self, parser:ConfigParser):
        self.parser   = parser

    @abstractmethod
    def get_data(self) -> object:
        pass
    
    @abstractmethod
    def set_data(self, value:object) ->bool:
        pass


class FileSettingParser(SettingParser):

    def get_data(self) -> object:
        return FileSetting(self.parser.data['content path'])
    
    def set_data(self, value:object) ->bool:
        self.parser.data['content path'] = value
        return True


class SettingParserData(NamedTuple):
    setting : object
    parser  : SettingParser
