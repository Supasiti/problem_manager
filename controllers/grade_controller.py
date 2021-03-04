from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from models.grade_area_model import GradeAreaModel, GradeAreaDataBuilder, GradeCountsDataBuilder  
from views.scroll_area import GradeArea

class GradeAreaController():
    # controller all interaction the top station

    _dependency : DependencyService
    _editor         : ProblemsEditor

    def __init__(self, dependency):
        self._setup_dependencies(dependency)           
        self.model = GradeAreaModel()            # load model
        self.view  = GradeArea(self, self.model) # load view
        self._connect_editor()
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._editor     = self._dependency.get(ProblemsEditor)

    def _connect_editor(self):
        self._editor.problemsChanged.connect(self._on_problems_changed)
        self._editor.problemAdded.connect(self._on_problems_changed)
        self._editor.problemRemoved.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        self.model.update_counts(self._editor.problems)
