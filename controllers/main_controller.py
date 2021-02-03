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

    def print_cell_info(self, row, col):
        print ('row: %s, column: %s' % (row, col))