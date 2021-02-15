from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt 
from datetime import date

from models.tool_model import ToolDynamicData
from APImodels.colour import Colour
from views.frame import FixedWidthFrame
from views.label import FixedSizeLabel

class ToolStation(FixedWidthFrame):

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        self.width = self.model.static_data.width
        super().__init__(self.width)
    
        self._init__UI()
        self._set_data()
        self._connect_model()

    def _init__UI(self):
        label_title = FixedSizeLabel(self.width -6, 40, 'Problem Editor')
        label_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label_title.set_colours(Colour(30,30,30), Colour(240,240,240))

        label_id = FixedSizeLabel(80, 28, 'Id:')
        label_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_ric = FixedSizeLabel(80, 28, 'RIC:')
        label_ric.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_grade = FixedSizeLabel(80, 28, 'Grade:')
        label_grade.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_hold = FixedSizeLabel(80, 28, 'Hold Colour:')
        label_hold.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_sector = FixedSizeLabel(80, 28, 'Sector:')
        label_sector.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_styles = FixedSizeLabel(80, 28, 'Styles:')
        label_styles.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_set_by = FixedSizeLabel(80, 28, 'Set by:')
        label_set_by.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_set_date = FixedSizeLabel(80, 28, 'Set Date:')
        label_set_date.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_status = FixedSizeLabel(80, 28, 'Status:')
        label_status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_buffer = QLabel()

        self.button_update = QPushButton('Update')
        self.button_update.mousePressEvent = self._update_problem

        # editing side
        self.text_id = FixedSizeLabel(190, 28)
        self.text_id.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.dropdown_r = QComboBox()
        self.dropdown_r.addItems(['1','2','3','4','5'])

        self.dropdown_i = QComboBox()
        self.dropdown_i.addItems(['1','2','3','4','5'])

        self.dropdown_c = QComboBox()
        self.dropdown_c.addItems(['1','2','3','4','5'])

        self.text_grade  = FixedSizeLabel(190, 28)
        self.text_grade.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.text_sector = FixedSizeLabel(190, 28)
        self.text_sector.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.dropdown_hold = QComboBox() 
        self.dropdown_status = QComboBox() 
        self.dropdown_status.addItems(['On', 'Stripped'])

        self.lineedit_styles_0 = QLineEdit()
        self.lineedit_styles_1 = QLineEdit()
        self.lineedit_styles_2 = QLineEdit()
        self.lineedit_set_by   = QLineEdit()
        self.lineedit_set_date = QLineEdit()
        self.lineedit_set_date.setPlaceholderText('YYYY-MM-DD')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(2,2,2,2)
        self.layout.setSpacing(8)
        self.layout.addWidget(label_title,    0, 0, 1, 4)
        self.layout.addWidget(label_id,       1, 0)
        self.layout.addWidget(label_ric,      2, 0)
        self.layout.addWidget(label_grade,    3, 0)
        self.layout.addWidget(label_hold,     4, 0)
        self.layout.addWidget(label_sector,   5, 0)
        self.layout.addWidget(label_styles,   6, 0)
        self.layout.addWidget(label_set_by,   9, 0)
        self.layout.addWidget(label_set_date,10, 0)
        self.layout.addWidget(label_status,  11, 0)
        self.layout.addWidget(label_buffer,  13, 0)

        self.layout.addWidget(self.text_id,       1, 1, 1, 3)
        self.layout.addWidget(self.dropdown_r,    2, 1)
        self.layout.addWidget(self.dropdown_i,    2, 2)
        self.layout.addWidget(self.dropdown_c,    2, 3)
        self.layout.addWidget(self.text_grade,    3, 1, 1, 3)
        self.layout.addWidget(self.dropdown_hold, 4, 1, 1, 3)
        self.layout.addWidget(self.text_sector,   5, 1, 1, 3)
        self.layout.addWidget(self.lineedit_styles_0, 6, 1, 1, 3)
        self.layout.addWidget(self.lineedit_styles_1, 7, 1, 1, 3)
        self.layout.addWidget(self.lineedit_styles_2, 8, 1, 1, 3)
        self.layout.addWidget(self.lineedit_set_by,   9, 1, 1, 3)
        self.layout.addWidget(self.lineedit_set_date,10, 1, 1, 3)
        self.layout.addWidget(self.dropdown_status,  11, 1, 1, 3)
        self.layout.addWidget(self.button_update,    12, 2, 1, 2)   
        self.setLayout(self.layout)

    def _set_data(self):
        data = self.model.dynamic_data
        _problem = data.problem
        self.text_id.setText(str(_problem.id))
        self.dropdown_r.setCurrentText(str(_problem.RIC.R))
        self.dropdown_i.setCurrentText(str(_problem.RIC.I))
        self.dropdown_c.setCurrentText(str(_problem.RIC.C))
        self.text_grade.setText(str(_problem.grade))
        self._set_dropdown_hold(data)
        self.text_sector.setText(_problem.sector.upper())
        self._set_lineedit_styles(_problem.styles)
        self.lineedit_set_by.setText(_problem.set_by)
        self._set_lineedit_set_date(_problem.set_date)
        self.dropdown_status.setCurrentText(_problem.status)

    def _set_dropdown_hold(self, data:ToolDynamicData):
        self.dropdown_hold.clear()
        self.dropdown_hold.addItems(data.holds)
        self.dropdown_hold.setCurrentText(data.problem.colour)
        return True

    def _set_lineedit_styles(self, styles:tuple[str,...]):
        for index in range(3):
            _lineedit = getattr(self, 'lineedit_styles_' + str(index))
            _lineedit.setText(styles[index]) if len(styles) > index else _lineedit.setText('')

    def _set_lineedit_set_date(self, _date:date = None):
        if _date is None:
            self.lineedit_set_date.setText('')
            return True
        self.lineedit_set_date.setText(_date.isoformat())
        return True

    def _connect_model(self):
        self.model.dataChanged.connect(self._set_data)
        return True

    def _update_problem(self, event):
        self.controller.update_problem()
        