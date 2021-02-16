
from models.bottom_model import BottomStationModel 
from views.bottom_station import BottomStation
from services.problems_editor import ProblemsEditor
from services.contents_path_manager import ContentsPathManager

class BottomController():
    # controller all interaction the bottom station

    def __init__(self, dependency, parent=None):
        self._parent     = parent
        self._dependency = dependency

        self.model = BottomStationModel()            # load model
        self.view  = BottomStation(self, self.model) # load view
        self.open_directory(self.model.dynamic_data) 

    def open_directory(self, directory:str =None):
        if directory is None:
            directory = self.get_directory()
        path_manager  = self._dependency.get(ContentsPathManager)  
        editor        = self._dependency.get(ProblemsEditor)  
        self.model.dynamic_data = directory
        path_manager.directory  = directory
        editor.load_problems_from_filepath(path_manager.filepath)

    def get_directory(self):
        return self.view.path_info.text()