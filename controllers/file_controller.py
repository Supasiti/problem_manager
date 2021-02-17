
from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from services.contents_path_manager import ContentsPathManager
from models.file_model import FileData, FileViewModel
from views.file_view import FileView

class FileController():
    # controller all interactions with file viewer

    _dependency     : DependencyService
    _editor         : ProblemsEditor

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)

        self.model = FileViewModel(data = FileData(tuple())) # load model
        self.view  = FileView(self, self.model)               # load view
        self.view.hide()
        self._connect_other()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)
        self._path_manager   = self._dependency.get(ContentsPathManager)
    
    def _connect_other(self):
        self._editor.stateChanged.connect(self._on_state_changed)

    def _on_state_changed(self, state_name:str):
        if state_name == 'editing':
            self.view.hide()
        elif state_name == 'viewing':
            self.view.show()
            self.model.view_data = FileData(tuple(self._path_manager.filenames))
        else:
            raise ValueError('incorrect state')
    
    def on_item_clicked(self, item_text:str):
        self._path_manager.filename = item_text
        self._editor.load_problems_from_filepath(self._path_manager.filepath)

