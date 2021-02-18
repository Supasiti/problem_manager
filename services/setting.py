import json
import os

class ConfigParser():
    # read/write configure file on loading / change

    _config_data : dict

    def __init__(self, filepath:str):
        self._filepath = filepath
        self.load_config(self._filepath)
        

    def load_config(self, filepath:str):
        with open(filepath, 'r') as fid:
            self._config_data = json.loads(fid.read())
            print(self._config_data)


class Setting():
    # filepath of config.json file is expected to be in the same folder as this class.
    
    def __init__(self):
        self._filepath     = self._create_filepath()
        self._parser       = ConfigParser(self._filepath)
        self._setting_dict = dict()

    def _create_filepath(self):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, 'config.json')

    def get(self, class_type:type) -> object:
        if class_type in self._setting_dict.keys():
            return self._setting_dict[class_type]
        return None


if __name__ == "__main__":

    setting = Setting()
