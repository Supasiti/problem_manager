from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt 

from APImodels.colour import Colour
from APImodels.problem import Problem
from models.problem_list_model import ProblemListCellData


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

        self._label_id  = QLabel()
        self._label_id.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_R = QLabel()
        self._label_R.setFixedWidth(32)
        self._label_R.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_I = QLabel()
        self._label_I.setFixedWidth(32)
        self._label_I.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._label_C = QLabel()
        self._label_C.setFixedWidth(32)
        self._label_C.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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
        layout.addWidget(self._label_R)
        layout.addWidget(self._label_I)
        layout.addWidget(self._label_C)
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
        
    def set_problem_data(self, problem:Problem):
        if not problem is None:
            self._label_id.setText(str(problem.id))
            self._label_R.setText(str(problem.RIC.R))
            self._label_I.setText(str(problem.RIC.I))
            self._label_C.setText(str(problem.RIC.C))
            self._label_grade.setText(str(problem.grade))
            self._label_colour.setText(str(problem.colour))
            self._set_style_text(problem)
            self._label_set_by.setText(str(problem.set_by))
            self._label_set_date.setText(problem.set_date.isoformat())
            self._label_strip_date.setText(problem.strip_date.isoformat())
        else:
            self._label_id.setText('')
            self._label_R.setText('')
            self._label_I.setText('')
            self._label_C.setText('')
            self._label_grade.setText('')
            self._label_colour.setText('')
            self._label_style0.setText('')
            self._label_style1.setText('')
            self._label_style2.setText('')
            self._label_set_by.setText('')
            self._label_set_date.setText('')
            self._label_strip_date.setText('')

    def _set_style_text(self,problem:Problem):
        styles = problem.styles
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


class ListCellHeader(QLabel):

    def __init__(self, data: ProblemListCellData, parent=None):
        super().__init__(parent=parent)
        self._clicked_command = None
        self.height = data.height
        self.width  = data.width
        self.setFixedHeight(self.height) 
        self.setMinimumWidth(self.width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 
        self._init_UI()
        self.set_data(data)

    def _init_UI(self):
        self.layout = QHBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(20,2,20,2)

        self._label_id  = ListCellHeaderLabel('Id', self._clicked_command)
        self._label_R   = ListCellHeaderLabel('R', self._clicked_command)
        self._label_R.setFixedWidth(32)
        self._label_I   = ListCellHeaderLabel('I', self._clicked_command)
        self._label_I.setFixedWidth(32)
        self._label_C   = ListCellHeaderLabel('C', self._clicked_command)
        self._label_C.setFixedWidth(32)
        self._label_grade = ListCellHeaderLabel('Grade', self._clicked_command)
        self._label_colour = ListCellHeaderLabel('Colour', self._clicked_command)
        self._label_style0 = ListCellHeaderLabel('Styles', self._clicked_command)
        self._label_style1 = QLabel()
        self._label_style2 = QLabel()
        self._label_set_by = ListCellHeaderLabel('Setter', self._clicked_command)
        self._label_set_date = ListCellHeaderLabel('Set on', self._clicked_command)
        self._label_strip_date = ListCellHeaderLabel('Stripped on', self._clicked_command)
        
        self.layout.addWidget(self._label_id)
        self.layout.addWidget(self._label_R)
        self.layout.addWidget(self._label_I)
        self.layout.addWidget(self._label_C)
        self.layout.addWidget(self._label_grade)
        self.layout.addWidget(self._label_colour)
        self.layout.addWidget(self._label_style0)
        self.layout.addWidget(self._label_style1)
        self.layout.addWidget(self._label_style2)
        self.layout.addWidget(self._label_set_by)
        self.layout.addWidget(self._label_set_date)
        self.layout.addWidget(self._label_strip_date)
        self.setLayout(self.layout)
    
    def set_data(self, data:ProblemListCellData):
        self._data = data
        self._set_colours(self._data.bg_colour, self._data.text_colour)
        self._add_mouse_effect()

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


    def set_clicked_command(self, command):
        self._clicked_command = command
        self._label_id.set_clicked_command(command)
        self._label_R.set_clicked_command(command)
        self._label_I.set_clicked_command(command)
        self._label_C.set_clicked_command(command)
        self._label_grade.set_clicked_command(command)
        self._label_colour.set_clicked_command(command)
        self._label_style0.set_clicked_command(command)
        self._label_set_by.set_clicked_command(command)
        self._label_set_date.set_clicked_command(command)
        self._label_strip_date.set_clicked_command(command)



class ListCellHeaderLabel(QLabel):

    def __init__(self, text:str, clicked_command=None):
        super().__init__(text)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._clicked_command = clicked_command
        self._add_mouse_effect()

    def _add_mouse_effect(self):
        self.setFocusPolicy(Qt.StrongFocus)

        if not self._clicked_command is None:
            self.mousePressEvent = self._on_mouse_clicked
    
    def _on_mouse_clicked(self, event):
        if not self._clicked_command is None:
            self._clicked_command(self.text())
    
    def set_clicked_command(self, command):
        self._clicked_command = command
        self.mousePressEvent = self._on_mouse_clicked