
from models.bottom_model import BottomStationModel 
from views.bottom_station import BottomStation
from services.problems_editor import ProblemsEditor, EditingProblemsEditor
from services.contents_path_manager import ContentsPathManager
from services.dependency_service import DependencyService
from services.file_setting import FileSetting
from services.setting import Setting

class BottomController():
    # controller all interaction the bottom station

    _dependency   : DependencyService
    _path_manager : ContentsPathManager
    _editor       : ProblemsEditor
    _setting      : Setting
    _file_setting : FileSetting

    def __init__(self, dependency:DependencyService):
        self._setup_dependencies(dependency)
        data       = self._setting.get(FileSetting).content_path
        self.model = BottomStationModel(dynamic_data = data)  # load model
        self.view  = BottomStation(self, self.model)      # load view
        self.open_directory(self.model.dynamic_data) 
        self._connect_other()

    def _setup_dependencies(self, dependency:DependencyService) -> None:
        self._dependency   = dependency
        self._path_manager = self._dependency.get(ContentsPathManager) 
        self._editor       = self._dependency.get(ProblemsEditor) 
        self._setting      = self._dependency.get(Setting)

    def open_directory(self, directory:str =None) ->None:
        if directory is None:
            directory = self.get_directory()
        if directory != self._setting.get(FileSetting).content_path:
            self._setting.update(FileSetting, directory)

        self._editor.change_to_state(EditingProblemsEditor())
        self.model.dynamic_data       = directory
        self._path_manager.directory  = directory
        self._editor.load_problems_from_filepath(self._path_manager.filepath)

    def get_directory(self) ->None:
        return self.view.path_info.text()

    def _connect_other(self) -> None:
        self._setting.settingChanged.connect(self._on_file_setting_changed)

    def _on_file_setting_changed(self, class_type:type) -> None:
        if class_type == FileSetting:
            value = self._setting.get(FileSetting).content_path
            if self.model.dynamic_data != value:  
                self.model.dynamic_data = value