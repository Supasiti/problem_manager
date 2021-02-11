
from models.work_model import WorkStationModel, WorkDynamicData 
from views.work_station import WorkStation
from controllers.problem_controller import ProblemAreaController
from controllers.sector_controller import SectorAreaController
from controllers.grade_controller import GradeAreaController

class WorkController():
    # controller all interaction the work station

    def __init__(self, dependency, parent):
        self.__parent   = parent
        self.dependency = dependency
        
        # load other controllers
        # self.info_controller    = None
        self.sector_controller = SectorAreaController(self.dependency, self)
        self.grade_controller  = GradeAreaController(self.dependency, self)
        self.problem_controller = ProblemAreaController(self.dependency, self)

        # build view data 
        view_data = WorkDynamicData(
            self.sector_controller.view,
            self.grade_controller.view,
            self.problem_controller.view
        )

        self.model = WorkStationModel(dynamic_data = view_data) # load model
        self.view  = WorkStation(self, self.model) # load view
    
    def on_content_path_changed(self, directory:str):
        # call when content path changes
        self.problem_controller.update_all_cells(directory)
        self.sector_controller.update_all_cells(directory)

    def on_problem_cell_clicked(self, problem_id:int, row:int, col:int):
        self.__parent.on_problem_cell_clicked(problem_id, row, col)