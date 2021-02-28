from services.dependency_service import DependencyService
from services.contents_path_manager import ContentsPathManager
from services.old_problem_IO import OldProblemIO
from services.old_problem_viewer import OldProblemViewer
from services.setting import Setting
from services.colour_setting import ColourSetting
from models.problem_list_model import ProblemListModel, ProblemListDataBuilder
from views.problem_list_view import ProblemListView

class ProblemListController():

    _dependency   : DependencyService

    def __init__(self,dependency:DependencyService):
        self._setup_dependencies(dependency)
        self._builder = ProblemListDataBuilder(self._colour_setting)
        self.model    = ProblemListModel()
        self.view     = ProblemListView(self, self.model)
        self._set_view_data(True)
        self._connect_other()

    def _setup_dependencies(self, dependency: DependencyService):
        self._dependency = dependency
        self._path_manager = self._dependency.get(ContentsPathManager)
        self._IO     = self._dependency.get(OldProblemIO)
        self._viewer = self._dependency.get(OldProblemViewer)
        directory    = self._path_manager.history_dir
        self._IO.set_dir(directory)
        self._viewer.set_dir_IO(self._IO)
        self._setting        = self._dependency.get(Setting)
        self._colour_setting = self._setting.get(ColourSetting)

    def _connect_other(self):
        self._viewer.problemsChanged.connect(self._set_view_data)

    def _set_view_data(self, arg:bool)->None:
        self.model.data = self._builder.from_problems(self._viewer.problems)

    def sort_by(self, text:str):
        print(text)

    
       