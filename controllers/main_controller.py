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
