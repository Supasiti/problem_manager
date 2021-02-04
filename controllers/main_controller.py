# Main controller
# 
# Aims:
#  - controls interactions with main view
#
from PyQt5.QtCore import QObject


class MainController(QObject):    

    def __init__(self, presenter):
        super().__init__()

        self.presenter = presenter

    def print_cell_info(self, problem_id):
        print ('Id: %s' % (problem_id))