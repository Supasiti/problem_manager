
from views.frame import FixedWidthFrame

class ToolStation(FixedWidthFrame):

    def __init__(self, controller):
        super().__init__(280)
        self.controller = controller
    