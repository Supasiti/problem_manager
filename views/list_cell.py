from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from models.problem_list_model import ProblemListCellData
from views.label import FixedSizeLabel

class ListCell(QLabel):
    
    _data : ProblemListCellData

    def __init__(self, data: ProblemListCellData):
        super().__init__()
        self.height = data.height
        self.width  = data.width
        self.setFixedHeight(self.height) 
        self.setMinimumWidth(self.width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 
        self._init_UI()
        self.set_data(data)
    
    def _init_UI(self):
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(20,2,20,2)

        self._label_id  = FixedSizeLabel(48, self.height)
        self._label_id.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_RIC = FixedSizeLabel(80, self.height)
        self._label_RIC.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self._label_grade = QLabel()
        self._label_grade.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_colour = QLabel()
        self._label_colour.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_style0 = QLabel()
        self._label_style0.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_style1 = QLabel()
        self._label_style1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_style2 = QLabel()
        self._label_style2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_set_by = QLabel()
        self._label_set_by.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_set_date = QLabel()
        self._label_set_date.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_strip_date = QLabel()
        self._label_strip_date.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(self._label_id)
        layout.addWidget(self._label_RIC)
        layout.addWidget(self._label_grade)
        layout.addWidget(self._label_colour)
        layout.addWidget(self._label_style0)
        layout.addWidget(self._label_style1)
        layout.addWidget(self._label_style2)
        layout.addWidget(self._label_set_by)
        layout.addWidget(self._label_set_date)
        layout.addWidget(self._label_strip_date)
        self.setLayout(layout)

    def set_data(self, data:ProblemListCellData):
        self._data = data
        self._set_colours(self._data.bg_colour, self._data.text_colour)
        self._add_mouse_effect()
        
        problem = self._data.problem
        if not problem is None:
            self._label_id.setText(str(problem.id))
            self._label_RIC.setText(str(problem.RIC))
            self._label_grade.setText(str(problem.grade))
            self._label_colour.setText(str(problem.colour))
            self._set_style_text()
            self._label_set_by.setText(str(problem.set_by))
            self._label_set_date.setText(problem.set_date.isoformat())
            self._label_strip_date.setText(problem.strip_date.isoformat())
        else:
            self._label_id.setText('Id')
            self._label_RIC.setText('RIC')
            self._label_grade.setText('Grade')
            self._label_colour.setText('Colour')
            self._label_style0.setText('Styles')
            self._label_style1.setText('')
            self._label_style2.setText('')
            self._label_set_by.setText('Setter')
            self._label_set_date.setText('Set on')
            self._label_strip_date.setText('Stripped on')
        

    def _set_style_text(self):
        styles = self._data.problem.styles
        style0 = str(styles[0])
        style1 = str(styles[1]) if len(styles) >=2 else ''
        style2 = str(styles[1]) if len(styles) ==3 else ''
        self._label_style0.setText(style0)
        self._label_style1.setText(style1)
        self._label_style2.setText(style2)

    def _set_colours(self, colour: Colour, text_colour: Colour):
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(colour.red, colour.green, colour.blue))
        pal.setColor(QPalette.WindowText, QColor(text_colour.red, text_colour.green, text_colour.blue))
        self.setPalette(pal)

    def _add_mouse_effect(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.enterEvent  = self._add_hover_effect
        self.leaveEvent  = self._remove_hover_effect

    def _add_hover_effect(self, event):
        self._set_colours(self._data.hover_colour, self._data.text_colour)
    
    def _remove_hover_effect(self, event):
        self._set_colours(self._data.bg_colour, self._data.text_colour)

