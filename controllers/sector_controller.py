
from services.problem_request import ProblemRequest
from services.dependency_service import DependencyService
from models.sector_area_model import SectorAreaModel, SectorAreaDataBuilder  
from models.dicts import SectorDict,ColourDict
from views.scroll_area import SectorArea

class SectorAreaController():
    # controller all interaction the top station

    _dependency : DependencyService
    _colour_setting : ColourDict
    _sector_setting : SectorDict

    def __init__(self, dependency : DependencyService, parent):
        self._parent  = parent
        self._setup_dependencies(dependency)
        self._builder = SectorAreaDataBuilder(self._sector_setting, self._colour_setting)
        self.model    = SectorAreaModel(self._builder.default())   # load model
        self.view     = SectorArea(self, self.model)               # load view
        self._connect_problem_request()
    
    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency = dependency
        self._colour_setting = self._dependency.get_or_register(ColourDict) 
        self._sector_setting = self._dependency.get_or_register(SectorDict)

    def _connect_problem_request(self):
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.problemsChanged.connect(self._on_problems_changed)
        problem_request.problemAdded.connect(self._on_problems_changed)
        problem_request.problemRemoved.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        problem_request    = self._dependency.get(ProblemRequest)
        self.model.changes = self._builder.from_problems(problem_request.problems)


