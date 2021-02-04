from PyQt5.QtCore import QObject
from presenters.dicts import GradeDict, SectorDict
from presenters.problem_cell_model import ProblemCellModelBuidler
from models.problem import Problem
from models.grade import Grade
from models.RIC import RIC
from datetime import date

class ProblemScrollAreaPresenter(QObject):

    def __init__(self, grade_setting: GradeDict, sector_setting: SectorDict):
        super().__init__()
        self.grade_setting = grade_setting
        self.sector_setting = sector_setting

        self.n_row = self.grade_setting.length()
        self.n_col = self.sector_setting.length()
        
        self.builder = ProblemCellModelBuidler()
        self.problems = [Problem(
            2, 
            RIC(1,2,3), 
            Grade('purple', 'mid'), 
            'purple',  
            'cave l', 
            ['pop', 'layback', 'power'], 
            'Thara', 
            date.today(),
            'on')]
        self.problem_cell_model_dict = self.__generate_cell_model_dictionary()
  

    def get_default_problem_cell_model(self, row:int, col:int):
        return self.builder.build_from_row_col(row,col)

    def __generate_cell_model_dictionary(self):
        # generate a dictionary containing (row, column) as keys, and problem cell models
        # as values
        models =  [self.__model(problem) for problem in self.problems]
        return {(model.row, model.col): model for model in models}

    def __model(self, problem):
        return self.builder.build_from_problem(problem)