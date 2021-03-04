
from models.bottom_model import BottomStationModel 
from views.bottom_station import BottomStation
from services.dependency_service import DependencyService
from services.file_setting import FileSetting
from services.setting import Setting

class BottomController():
    # controller all interaction the bottom station

    _dependency   : DependencyService
    _file_setting : FileSetting

    def __init__(self, dependency:DependencyService):
        self._setup_dependencies(dependency)
        data       = Setting.get(FileSetting).content_path
        self.model = BottomStationModel(dynamic_data = data)  # load model
        self.view  = BottomStation(self, self.model)      # load view
        self._connect_other()

    def _setup_dependencies(self, dependency:DependencyService) -> None:
        self._dependency   = dependency 

    def set_new_directory(self, directory:str ='') ->None:
        if directory == '':
            return
        if directory != Setting.get(FileSetting).content_path:
            Setting.update(FileSetting, directory)

    def get_directory(self) ->None:
        return self.view.path_info.text()

    def _connect_other(self) -> None:
        Setting.settingChanged.connect(self._on_file_setting_changed)

    def _on_file_setting_changed(self, class_type:type) -> None:
        if class_type == FileSetting:
            value = Setting.get(FileSetting).content_path
            if self.model.dynamic_data != value:  
                self.model.dynamic_data = value