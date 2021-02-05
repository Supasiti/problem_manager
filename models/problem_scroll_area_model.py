from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

from models.dicts import GradeDict, SectorDict
from models.problem_cell_model import ProblemCellModelBuilder
from APImodels.problem import Problem

class ProblemScrollAreaModel(QObject):

    cellModelsChanged = pyqtSignal(bool)
    cell_models = {} 

    def __init__(self, grade_setting: GradeDict, sector_setting: SectorDict):
        super().__init__()
        self.grade_setting = grade_setting
        self.sector_setting = sector_setting
        self.builder = ProblemCellModelBuilder()

        self.n_row = self.grade_setting.length()
        self.n_col = self.sector_setting.length()
        
        self._problems = tuple()


    @property
    def problems(self):
        return self._problems

    @problems.setter
    def problems(self, value:tuple[Problem,...]):
        self._problems = value
        self.cell_models = self.__generate_cell_model_dictionary()
        self.cellModelsChanged.emit(True)

    def get_default_problem_cell_model(self, row:int, col:int):
        return self.builder.build_from_row_col(row,col)

    def __generate_cell_model_dictionary(self):
        # generate a dictionary containing (row, column) as keys, and problem cell models
        # as values
        models =  [self.__model(problem) for problem in self.problems]
        return dict({(model.row, model.col): model for model in models})

    def __model(self, problem:Problem):
        return self.builder.build_from_problem(problem)

    def add_problems(self, problems:tuple[Problem,...]):
        # can't just add problems
        # need to replace old problems with the same id with new ones
        new_prob = list(problems)
        if len(new_prob) == 0:
            raise ValueError('add_problem() do not accept empty tuple.')
        if len(self.problems) != 0:
            old_prob = list(self.problems)
            new_ids  = {p.id for p in new_prob}
            old_prob = [p for p in old_prob if not p.id in new_ids]
            new_prob += old_prob
        self.problems = tuple(new_prob)
    
    def add_problem(self, problem:Problem):
        pass
