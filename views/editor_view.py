from PyQt5.QtWidgets import QFormLayout, QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt 
from datetime import date

from models.editor_model import EditorData
from APImodels.colour import Colour
from views.label import FixedSizeLabel

class EditorView(FixedSizeLabel):

    def __init__(self, controller, model): 
        self.controller = controller
        self.model      = model
        self.width      = self.model.static_data.width
        self.height     = self.model.static_data.height
        super().__init__(self.width, self.height)
    
        self._init__UI()
        self._set_data()
        self._connect_model()

    def _init__UI(self):
        label_title = FixedSizeLabel(self.width -6, 40, 'Problem Editor')
        label_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label_title.set_colours(Colour(30,30,30), Colour(240,240,240))

        label_id = FixedSizeLabel(80, 28, 'Id:')
        label_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # buttons
        self.button_update = QPushButton('Update')
        self.button_update.clicked.connect(self._update_problem)

        self.button_delete = QPushButton('&Delete')
        self.button_delete.clicked.connect(self._delete_problem)
        self.button_delete.setShortcut('Ctrl+D')

        self.button_strip = QPushButton('Strip')
        self.button_strip.clicked.connect(self._strip_problem)
        self.button_strip.setShortcut('Ctrl+Shift+D')
        
        self.layout_button = QGridLayout()
        self.layout_button.addWidget(self.button_update,   0, 1)   
        self.layout_button.addWidget(self.button_delete,   0, 0)
        self.layout_button.addWidget(self.button_strip,    0, 0)

        # editing side
        self.text_id = FixedSizeLabel(190, 28)
        self.text_id.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.dropdown_r = QComboBox()
        self.dropdown_r.addItems(['1','2','3','4','5'])

        self.dropdown_i = QComboBox()
        self.dropdown_i.addItems(['1','2','3','4','5'])

        self.dropdown_c = QComboBox()
        self.dropdown_c.addItems(['1','2','3','4','5'])
        self.layout_combo = QHBoxLayout()
        self.layout_combo.addWidget(self.dropdown_r)
        self.layout_combo.addWidget(self.dropdown_i)
        self.layout_combo.addWidget(self.dropdown_c)

        self.text_grade  = FixedSizeLabel(190, 28)
        self.text_grade.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.text_sector = FixedSizeLabel(190, 28)
        self.text_sector.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.dropdown_hold = QComboBox() 

        self.lineedit_styles_0 = QLineEdit()
        self.lineedit_styles_1 = QLineEdit()
        self.lineedit_styles_2 = QLineEdit()
        self.lineedit_set_by   = QLineEdit()
        self.lineedit_set_date = QLineEdit()
        self.lineedit_set_date.setPlaceholderText('YYYY-MM-DD')
        self.lineedit_strip_date = QLineEdit()
        self.lineedit_strip_date.setPlaceholderText('YYYY-MM-DD')
        self.label_strip_date = FixedSizeLabel(80, 28, 'Strip Date:')
        self.label_strip_date.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # layout
        self.layout = QFormLayout()
        self.layout.setFormAlignment(Qt.AlignTop)
        self.layout.setLabelAlignment(Qt.AlignRight)
        self.layout.setContentsMargins(2,2,2,2)
        
        self.layout.addRow(label_title)
        self.layout.addRow(label_id,    self.text_id)
        self.layout.addRow('RIC:',   self.layout_combo)
        self.layout.addRow('Grade:', self.text_grade)
        self.layout.addRow('Hold Colour:', self.dropdown_hold)
        self.layout.addRow('Sector:',  self.text_sector)
        self.layout.addRow('Styles:',  self.lineedit_styles_0)
        self.layout.addRow('',         self.lineedit_styles_1)
        self.layout.addRow('',         self.lineedit_styles_2)
        self.layout.addRow('Set by:',  self.lineedit_set_by)
        self.layout.addRow('Set Date:',self.lineedit_set_date)
        self.layout.addRow(self.label_strip_date, self.lineedit_strip_date)
        self.layout.addRow(self.layout_button)
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
            
        if data.is_strippable:
            self.label_strip_date.show()
            self.lineedit_strip_date.show()
            self.button_strip.show()
        else:
            self.label_strip_date.hide()
            self.lineedit_strip_date.hide()
            self.button_strip.hide()

        if data.is_deletable:
            self.button_delete.show()
        else:
            self.button_delete.hide()

        if data.is_addable:
            self.button_update.show()
        else:
            self.button_update.hide()


    def _set_dropdown_hold(self, data:EditorData):
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

    def _delete_problem(self, event):
        self.controller.delete_problem()
    
    def _strip_problem(self, event):
        self.controller.strip_problem()
        