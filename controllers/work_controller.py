from services.problems_editor import ProblemsEditor
from services.setting import Setting
from services.grade_setting import GradeSetting
from models.work_model import WorkStationModel, WorkDynamicData 
from views.work_station import WorkStation
from controllers.problem_controller import ProblemAreaController
from controllers.sector_controller import SectorAreaController
from controllers.grade_controller import GradeAreaController

class WorkController():
    # controller all interaction the work station

    def __init__(self, dependency, parent=None):
        self._parent     = parent
        self._dependency = dependency
        self._editor     = self._dependency.get(ProblemsEditor)
        
        # load other controllers
        self.sector_controller  = SectorAreaController(self._dependency)
        self.grade_controller   = GradeAreaController(self._dependency)
        self.problem_controller = ProblemAreaController(self._dependency)

        # build view data 
        view_data = WorkDynamicData(
            self.sector_controller.view,
            self.grade_controller.view,
            self.problem_controller.view
        )

        self.model = WorkStationModel(dynamic_data = view_data) # load model
        self.view  = WorkStation(self, self.model)              # load view
        self._connect_editor()
        self._set_aim()
        self._set_count()

    def _set_aim(self):
        grade_setting = Setting.get(GradeSetting)
        aim           = grade_setting.get_total_aim()
        self.view.info_view.set_aim(aim)
    
    def _set_count(self):
        count = len(self._editor.problems)
        self.view.info_view.set_count(count)

    def _connect_editor(self):
        self._editor.problemsChanged.connect(self._on_problems_changed)
        self._editor.problemAdded.connect(self._on_problems_changed)
        self._editor.problemRemoved.connect(self._on_problems_changed)

    def _on_problems_changed(self, arg:bool):
        self._set_count()
