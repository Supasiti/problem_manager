
from views.frame import FixedWidthFrame

class ToolStation(FixedWidthFrame):

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        super().__init__(self.model.static_data.width)
    