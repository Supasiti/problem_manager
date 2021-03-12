# Main application gateway
#
import sys

from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController
from services.dependency_service import DependencyService
from services.contents_path_manager import ContentsPathManager
from services.problem_repository import LocalProblemRepository
from services.json_writer import JsonWriter, StrippedProblemWriter
from services.old_problem_viewer import OldProblemViewer
from services.old_problem_IO import OldProblemIO
from services.sector_editor import SectorEditor

'''
    Application
'''

class App(QApplication):
    
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.dependency = DependencyService()
        self.dependency.register(ContentsPathManager)
        self.dependency.register(JsonWriter)
        self.dependency.register(LocalProblemRepository)
        self.dependency.register(StrippedProblemWriter)
        self.dependency.register(OldProblemIO)
        self.dependency.register(OldProblemViewer)
        self.dependency.register(SectorEditor)

        self.main_controller = MainController(self.dependency)

if __name__ == '__main__':
    app = App(sys.argv)
    app.setStyle('Fusion')
    # app.setStyle('Macintosh')
    sys.exit(app.exec_())   
