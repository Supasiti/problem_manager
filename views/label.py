# template for fixed size/width/height label

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from models.problem_cell_data import ProblemCellData
from models.grade_area_model import GradeCellData, GradeCountData
from models.sector_area_model import SectorCellData


class FixedWidthLabel(QLabel):
    
    def __init__(self, width):
        super().__init__()
        self.setFixedWidth(width) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding) 
    
    def set_colours(self, 
        colour: Colour, text_colour: Colour):
        
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)


class FixedSizeLabel(QLabel):

    def __init__(self, width:int, height:int, text:str=''):
        super().__init__(text)
        self.setFixedWidth(width) 
        self.setFixedHeight(height) 
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 

    def set_colours(self, 
        colour: Colour, text_colour: Colour):
        
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)




class ProblemCell(QLabel):
    # cell displaying info on problem if there is no problem on this particular
    # cell. This is the base problem cell.

    _data : ProblemCellData

    def __init__(self, width:int, height:int, data: ProblemCellData):
        super().__init__()
        self._width  = width
        self._height = height
        self._init_UI()
        self._clicked_command = None
        self.set_data(data)
    
    # TODO width, height in problem cell data

    def _init_UI(self):
        self.setMinimumWidth(self._width) 
        self.setFixedHeight(self._height) 
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(2,2,2,2)
        self.text_style = QLabel()
        self.text_style.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.text_ric   = QLabel()
        self.text_ric.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.text_style)
        layout.addWidget(self.text_ric)
        self.setLayout(layout)

    def set_data(self, data: ProblemCellData):
        self._data = data
        self._set_colours(self._data.bg_colour, self._data.text_colour)
        self._add_mouse_effect()
        self.text_style.setText(self._data.text)
        self.text_ric.setText(self._data.RIC)
    
    def _add_mouse_effect(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.enterEvent  = self._add_hover_effect
        self.leaveEvent  = self._remove_hover_effect

        if not self._clicked_command is None:
            self.mousePressEvent = self._on_mouse_clicked
    
    def _on_mouse_clicked(self, event):
        if not self._clicked_command is None:
            self._clicked_command(self._data.id, self._data.row, self._data.col)
    
    def _add_hover_effect(self, event):
        self._set_colours(self._data.hover_colour, self._data.text_colour)
    
    def _remove_hover_effect(self, event):
        self._set_colours(self._data.bg_colour, self._data.text_colour)

    def set_clicked_command(self, command):
        self._clicked_command = command
        self.mousePressEvent = self._on_mouse_clicked

    def _set_colours(self, colour: Colour, text_colour: Colour):
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)

class GradeCell(FixedSizeLabel):
    # cell displaying info related to the grade
    _data  : GradeCellData
    _count : GradeCountData

    def __init__(self, data : GradeCellData, count: GradeCountData ):
        super().__init__(data.width, data.height)
        self._init_UI(data)
        self.set_static_data(data)
        self.set_count_data(count)

    def _init_UI(self, data: GradeCellData):
        _data  = data
        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

        self.text_style = FixedSizeLabel(_data.inner_width, _data.inner_height)
        self.text_style.setText('Style')
        self.text_style.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.text_ric = FixedSizeLabel(_data.inner_width, _data.inner_height)
        self.text_ric.setText('RIC')
        self.text_ric.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 

        self.text_aim = FixedSizeLabel(_data.inner_width, _data.height)
        self.text_aim.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 

        self.text_count = FixedSizeLabel(_data.inner_width, _data.height)
        self.text_count.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 

        self.layout.addWidget(self.text_style, 0, 0)
        self.layout.addWidget(self.text_ric,   1, 0)
        self.layout.addWidget(self.text_aim,   0, 1, 2, 1)
        self.layout.addWidget(self.text_count, 0, 2, 2, 1)
        self.setLayout(self.layout)

    def set_static_data(self, data:GradeCellData):
        self._data = data
        self.text_style.set_colours(self._data.bg_colour, self._data.text_colour)
        self.text_ric.set_colours(self._data.bg_colour, self._data.text_colour)
        self.text_aim.setText(self._data.aim)
        self.text_aim.set_colours(self._data.bg_colour, self._data.text_colour)

    def set_count_data(self, data: GradeCountData):
        self._count = data
        self.text_count.setText(self._count.text)
        self.text_count.set_colours(self._count.bg_colour, self._count.text_colour)


class SectorCell(QLabel):
    # cell displaying info on each sector

    _data : SectorCellData

    def __init__(self, height:int, data:SectorCellData) -> None:
        super().__init__()
        self._width   = data.width
        self._height  = height
        self._popup_menu      = None
        self._clicked_command = None
        self._init_UI()
        self._add_mouse_effect()
        self.set_data(data)

    # TODO put width and height in SectorCellData
    def _init_UI(self) -> None:
        self.setMinimumWidth(self._width) 
        self.setFixedHeight(self._height) 
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(2,2,2,2)
        self.text_sector = QLabel()
        self.text_sector.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.text_count = QLabel()
        self.text_count.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.text_sector)
        layout.addWidget(self.text_count)
        self.setLayout(layout)

    def set_data(self, data:SectorCellData) -> None:
        self._data = data
        self._set_colours(self._data.bg_colour, self._data.text_colour)
        self.text_sector.setText(self._data.text)
        self.text_count.setText(self._data.problem_count)
    
    def _set_colours(self, colour: Colour, text_colour: Colour) -> None:
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)
    
    def _add_mouse_effect(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        if not self._popup_menu is None:
            self.customContextMenuRequested.connect(self._on_context_menu)
        if not self._clicked_command is None :
            self.mousePressEvent = self._on_mouse_clicked

    def _on_context_menu(self, point):
        self._popup_menu.exec_(self.mapToGlobal(point))  

    def set_context_menu(self, popup_menu:QMenu) -> None:
        self._popup_menu = popup_menu
        self.customContextMenuRequested.connect(self._on_context_menu)

    def _on_mouse_clicked(self, event):
        if not self._clicked_command is None:
            if event.button() == Qt.RightButton:
                self._clicked_command(self._data.col)
    
    def set_clicked_command(self, command):
        self._clicked_command = command
        self.mousePressEvent = self._on_mouse_clicked



class InfoCell(FixedSizeLabel):

    def __init__(self, controller, model):
        self.controller = controller
        self.model  = model
        self.width  = self.model.static_data.width
        self.height = self.model.static_data.height
        super().__init__(self.width, self.height)
        self._init_UI()
        self.set_aim(self.model.aim)

    def _init_UI(self):
        data = self.model.static_data

        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

        self.text_sector = FixedSizeLabel(data.inner_width, data.height,'Sectors')
        self.text_sector.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.text_sector.set_colours(data.bg_colour, data.text_colour)

        self.text_aim = FixedSizeLabel(data.inner_width, data.inner_height, 'Aim')
        self.text_aim.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        self.text_aim.set_colours(data.bg_colour, data.text_colour)

        self.label_aim = FixedSizeLabel(data.inner_width, data.inner_height)
        self.label_aim.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        self.label_aim.set_colours(data.bg_colour, data.text_colour)

        self.text_counts = FixedSizeLabel(data.inner_width, data.inner_height, 'Counts')
        self.text_counts.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        self.text_counts.set_colours(data.bg_colour, data.text_colour)

        self.label_count = FixedSizeLabel(data.inner_width, data.inner_height)
        self.label_count.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        self.label_count.set_colours(data.bg_colour, data.text_colour)

        self.layout.addWidget(self.text_sector, 0, 0, 2, 1)
        self.layout.addWidget(self.text_aim,    0, 1)
        self.layout.addWidget(self.text_counts, 0, 2)
        self.layout.addWidget(self.label_aim,   1, 1)
        self.layout.addWidget(self.label_count, 1, 2)

        self.setLayout(self.layout)

    def set_count(self, value:int)->None:
        self.label_count.setText(str(value))

    def set_aim(self,value:int) -> None:
        self.label_aim.setText(str(value))