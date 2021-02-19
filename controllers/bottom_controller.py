
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

        self.model = BottomStationModel(dynamic_data= self._file_setting.content_path)  # load model
        self.view  = BottomStation(self, self.model)      # load view
        self.open_directory(self.model.dynamic_data) 

    def _setup_dependencies(self, dependency:DependencyService) -> None:
        self._dependency   = dependency
        self._path_manager = self._dependency.get(ContentsPathManager) 
        self._editor       = self._dependency.get(ProblemsEditor) 
        self._setting      = self._dependency.get(Setting)
        self._file_setting = self._setting.get(FileSetting) 

    def open_directory(self, directory:str =None):
        if directory is None:
            directory = self.get_directory()
        if directory != self._file_setting.content_path:
            self._setting.update(FileSetting, directory)

        self._editor.change_to_state(EditingProblemsEditor())
        self.model.dynamic_data       = directory
        self._path_manager.directory  = directory
        self._editor.load_problems_from_filepath(self._path_manager.filepath)

    def get_directory(self):
        return self.view.path_info.text()