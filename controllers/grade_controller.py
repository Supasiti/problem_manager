from services.dependency_service import DependencyService
from services.problem_request import ProblemRequest
from models.grade_area_model import GradeAreaModel, GradeAreaDataBuilder, GradeCountsDataBuilder  
from models.dicts import GradeDict,ColourDict
from views.scroll_area import GradeArea

class GradeAreaController():
    # controller all interaction the top station

    _dependency : DependencyService
    _colour_setting : ColourDict
    _grade_setting : GradeDict

    def __init__(self, dependency, parent):
        self._parent         = parent
        self._setup_dependencies(dependency)
        self._builder        = GradeAreaDataBuilder(self._grade_setting, self._colour_setting)
        self._count_builder  = GradeCountsDataBuilder(self._grade_setting, self._colour_setting)             
        data   = self._builder.default()
        counts = self._count_builder.default()

        self.model = GradeAreaModel(data, counts)   # load model
        self.view  = GradeArea(self, self.model) # load view
        self._connect_problem_request()
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._colour_setting = self._dependency.get_or_register(ColourDict) 
        self._grade_setting = self._dependency.get_or_register(GradeDict)

    def _connect_problem_request(self):
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.problemsChanged.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        problem_request   = self._dependency.get(ProblemRequest)
        self.model.counts = self._count_builder.from_problems(problem_request.problems)

