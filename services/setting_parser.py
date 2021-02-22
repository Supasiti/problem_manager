from abc import ABC, abstractmethod
import json

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