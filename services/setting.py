from typing import NamedTuple
from threading import Lock

from services.signal import Signal
from services.setting_parser import SettingParser
from services.file_setting import FileSetting,   FileSettingParser
from services.grade_setting  import GradeSetting, GradeSettingParser
from services.colour_setting import ColourSetting, ColourSettingParser
from services.sector_setting import SectorSetting, SectorSettingParser

class SettingParserData(NamedTuple):
    setting : object
    parser  : SettingParser


class Setting():
    
    settingChanged = Signal(type)
    _padlock = Lock()
    _parsers = {
        FileSetting   : FileSettingParser, 
        GradeSetting  : GradeSettingParser,
        ColourSetting : ColourSettingParser,
        SectorSetting : SectorSettingParser
    }

    _settings = dict.fromkeys(_parsers.keys())

    @classmethod
    def get(cls, class_type:type) -> object:
        if class_type in cls._settings.keys():
            if cls._settings[class_type] is None:
                parser = cls._parsers[class_type]
                instance = parser()
                cls._register(class_type, instance.get_data(), instance)
            return cls._settings[class_type].setting
        return None

    @classmethod
    def _register(cls, class_type: type, setting:object, parser:object) -> bool:
        if isinstance(setting, class_type):
            with cls._padlock:
                cls._settings[class_type] = SettingParserData(setting, parser)
            return True
        raise ValueError('_register(): Trying to register an incorrect setting class.')
    
    @classmethod
    def update(cls, class_type:type, value:object) ->bool:
        if class_type in cls._settings.keys():
            parser = cls._settings[class_type].parser
            parser.set_data(value)
            cls._register(class_type, parser.get_data(), parser)
            cls.settingChanged.emit(class_type)
            return True
        raise ValueError('This setting has not been registered.')

    @classmethod
    def write(cls, class_type:type):
        if class_type in cls._settings.keys():
            parser = cls._settings[class_type].parser
            parser.write()

