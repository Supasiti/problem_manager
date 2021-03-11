
from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from services.contents_path_manager import ContentsPathManager
from services.problem_repository import LocalProblemRepository
from models.file_model import FileData, FileViewModel
from views.file_view import FileView

class FileController():
    # controller all interactions with file viewer

    _dependency : DependencyService
    _editor     : ProblemsEditor
    _repo       : LocalProblemRepository

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)

        self.model = FileViewModel()            # load model
        self.view  = FileView(self, self.model) # load view
        self._connect()
        self._show_filenames()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)
        self._path_manager   = self._dependency.get(ContentsPathManager)
        self._repo           = self._dependency.get(LocalProblemRepository)
    
    def _connect(self):
        self.model.dataChanged.connect(self.view.set_data)
    
    def _show_filenames(self):
        self.model.view_data = FileData(tuple(self._path_manager.filenames))

    def on_item_clicked(self, item_text:str):
        self._path_manager.filename = item_text
        self._repo.set_filepath(self._path_manager.filepath)
        self._editor.load_problems(self._repo)

