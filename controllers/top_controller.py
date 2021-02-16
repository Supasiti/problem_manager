from datetime import date

from services.dependency_service import DependencyService
from services.contents_path_manager import ContentsPathManager
from services.path_builder import PathBuilder
from models.top_model import TopStationModel 
from views.top_station import TopStation

class TopController():
    # controller all interaction the top station

    def __init__(self, dependency:DependencyService, parent=None):
        self._parent     = parent
        self._dependency = dependency
        self._dependency.register(PathBuilder)

        self.model = TopStationModel()            # load model
        self.view  = TopStation(self, self.model) # load view
        self._connect_editor()

    def _connect_editor(self):
        path_manager = self._dependency.get(ContentsPathManager)
        path_manager.filepathChanged.connect(self._on_filepath_changed)

    def _on_filepath_changed(self, filepath:str):
        path_manager = self._dependency.get(ContentsPathManager)
        self.model.date_str = path_manager.filename

    def get_filename(self):
        return self.view.date_lineedit.text()

    def update_filename_to_save(self):
        # return false if date is empty / incorrect format / same as current file
        path_manager = self._dependency.get(ContentsPathManager)
        date_str     = self.view.date_lineedit.text()
        if self._verify_date_string(date_str):
            path_manager.filename_to_save = date_str
            return True
        return False
        
    def _verify_date_string(self, date_str:str):
        # return false if date is empty / incorrect format / same as current file
        lineedit = self.view.date_lineedit
        if date_str == '':
            lineedit.setPlaceholderText('must have a date in YYYY-MM-DD')
            return False
        if not self._is_isoformat(date_str):
            lineedit.setText('')
            lineedit.setPlaceholderText('expect a date in format YYYY-MM-DD')
            return False
        if self._same_as_current_file(date_str):
            lineedit.setText('')
            lineedit.setPlaceholderText('must differ from current file')
            return False
        return True

    def _is_isoformat(self, date_str:str):
        # return true if it is in iso format
        try:
            date.fromisoformat(date_str)
            return True
        except ValueError:
            self.view.date_lineedit.setText('')
            self.view.date_lineedit.setPlaceholderText('expect a date in format YYYY-MM-DD')
            return False
        
    def _same_as_current_file(self, date_str:str):
        path_manager    = self._dependency.get(ContentsPathManager)
        return date_str == path_manager.filename