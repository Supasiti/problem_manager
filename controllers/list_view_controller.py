from services.dependency_service import DependencyService
from services.contents_path_manager import ContentsPathManager
from services.old_problem_IO import OldProblemIO
from services.old_problem_viewer import OldProblemViewer
from services.setting import Setting
from services.colour_setting import ColourSetting
from models.problem_list_model import ProblemListModel, ProblemListDataBuilder
from views.problem_list_view import ProblemListMainView

class ProblemListController():

    _dependency   : DependencyService
    _sort_dict = { 
        'Id' : lambda x : x.id,
        'R'  : lambda x : x.RIC.R,
        'I'  : lambda x : x.RIC.I,
        'C'  : lambda x : x.RIC.C,
        'Grade' : lambda x : str(x.grade),
        'Colour' : lambda x : x.colour,
        'Styles' : lambda x : x.styles[0],
        'Setter' : lambda x : x.set_by.lower(),
        'Set on' : lambda x : x.set_date,
        'Stripped on' : lambda x : x.strip_date
    }

    def __init__(self,dependency:DependencyService):
        self._setup_dependencies(dependency)
        self._builder = ProblemListDataBuilder(self._colour_setting)
        self.model    = ProblemListModel()
        self.view     = ProblemListMainView(self, self.model)
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
        self._colour_setting = Setting.get(ColourSetting)

    def _connect_other(self):
        self._viewer.problemsChanged.connect(self._set_view_data)

    def _set_view_data(self, arg:bool)->None:
        self.model.data = self._builder.from_problems(self._viewer.problems)

    def sort_by(self, text:str):
        if text in self._sort_dict.keys():
            sort_function = self._sort_dict[text]
            self.model.sort_problems_by(sort_function)
    
       