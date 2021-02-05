# Main controller
# 
# Aims:
#  - controls interactions with main view
#
from PyQt5.QtCore import QObject

from services.problem_request import ProblemRequest


class MainController(QObject):    

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.problem_request = ProblemRequest()
        
    def print_cell_info(self, problem_id):
        print('Problem id : %s' % problem_id)

    def open_directory(self, directory:str):
        
        self.model.bottom_model.content_path = directory
        
        problems = self.problem_request.get_all_current_problems(directory)
        self.model.problem_scroll_area_model.problems = problems

        sectors = self.problem_request.get_all_sectors(directory)
        self.model.sector_scroll_area_model.sectors = sectors
        