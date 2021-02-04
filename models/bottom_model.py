#  Model for the bottom station

from PyQt5.QtCore import QObject
import os

class BottomStationModel(QObject):

    def __init__(self):
        super().__init__()
        self.content_path = r'/Users/thara/Desktop/Programming/python/problem_manager/contents'

