import os

from services.setting_parser import SettingParser

class FileSetting():
    # contains all data related to file paths 

    def __init__(self, content_path:str):
        self._content_path = content_path

    @property
    def content_path(self) -> str:
        return self._content_path


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
