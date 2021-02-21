from typing import NamedTuple
from threading import Lock

from services.signal import Signal
from services.setting_parser import SettingParser
from services.file_setting import FileSetting,   FileSettingParser
from services.grade_setting  import GradeSetting, GradeSettingParser
from services.colour_setting import ColourSetting, ColourSettingParser
from services.sector_setting import SectorSetting, SectorSettingParser

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

class SettingParserData(NamedTuple):
    setting : object
    parser  : SettingParser
