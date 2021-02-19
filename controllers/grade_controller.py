from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from services.setting import Setting
from services.grade_setting import GradeSetting
from services.colour_setting import ColourSetting
from models.grade_area_model import GradeAreaModel, GradeAreaDataBuilder, GradeCountsDataBuilder  
from views.scroll_area import GradeArea

class GradeAreaController():
    # controller all interaction the top station

    _dependency : DependencyService
    _colour_setting : ColourSetting
    _grade_setting  : GradeSetting
    _editor         : ProblemsEditor

    def __init__(self, dependency, parent=None):
        self._parent         = parent
        self._setup_dependencies(dependency)
        self._builder        = GradeAreaDataBuilder(self._grade_setting)
        self._count_builder  = GradeCountsDataBuilder(self._grade_setting, self._colour_setting)             
        data   = self._builder.default()
        counts = self._count_builder.default()

        self.model = GradeAreaModel(data, counts)   # load model
        self.view  = GradeArea(self, self.model) # load view
        self._connect_editor()
        
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._editor         = self._dependency.get(ProblemsEditor)
        self._setting        = self._dependency.get(Setting)
        self._grade_setting  = self._setting.get(GradeSetting)
        self._colour_setting = self._setting.get(ColourSetting)

    def _connect_editor(self):
        self._editor.problemsChanged.connect(self._on_problems_changed)
        self._editor.problemAdded.connect(self._on_problems_changed)
        self._editor.problemRemoved.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        self.model.counts = self._count_builder.from_problems(self._editor.problems)

