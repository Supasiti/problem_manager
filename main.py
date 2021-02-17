# Main application gateway
#
import sys

from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController
from services.dependency_service import DependencyService

'''
    Application
'''

class App(QApplication):
    
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.dependency = DependencyService()
        self.main_controller = MainController(self.dependency)


if __name__ == '__main__':
    app = App(sys.argv)
    app.setStyle('Fusion')
    sys.exit(app.exec_()) 