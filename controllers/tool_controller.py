from datetime import date

from services.dependency_service import DependencyService
from services.problem_request import ProblemRequest
from models.tool_model import ToolStationModel, ToolDynamicData 
from models.dicts import ColourDict
from views.tool_station import ToolStation
from APImodels.problem import Problem
from APImodels.RIC import RIC
from APImodels.grade import Grade

class ToolController():
    # controller all interaction the tool station

    def __init__(self, dependency: DependencyService, parent:object):
        self._parent         = parent
        self._dependency     = dependency
        self._colour_setting = self._dependency.get_or_register(ColourDict)
        
        self.model = ToolStationModel(dynamic_data = self._view_data()) # load model
        self.view  = ToolStation(self, self.model)                      # load view
        self._connect_problem_request()

    def _connect_problem_request(self):
        problem_request = self._dependency.get(ProblemRequest)
        problem_request.problemToEditChanged.connect(self._on_problem_to_edit_changed)

    def _on_problem_to_edit_changed(self, arg:bool):
        problem_request         = self._dependency.get(ProblemRequest)
        problem_to_edit         = problem_request.problem_to_edit
        self.model.dynamic_data = self._view_data(problem_to_edit)
        return True

    def _view_data(self, problem:Problem = None):
        _problem  = Problem() if problem is None else problem
        grade_str = str(_problem.grade)
        holds     = self._colour_setting.get_hold_colours(grade_str)
        return ToolDynamicData(holds, _problem)

    def update_problem(self):
        _is_updatable = True
        _is_updatable = self._cell_selected()
        _is_updatable = self._prompt_if_form_incomplete()
        _problem      = self._make_problem() if _is_updatable else None
 
        if not _problem is None: 
            problem_request = self._dependency.get(ProblemRequest)
            problem_request.save_new_problem(_problem)
            self._reset_placeholder_texts()

    def _cell_selected(self):
        return self.view.text_id.text() != '' and self.view.text_sector.text() !=  '' 
        
    def _prompt_if_form_incomplete(self):
        # return True if the form is complete
        # otherwise False
        result = True
        if self.view.lineedit_styles_0.text()== '':
            self.view.lineedit_styles_0.setPlaceholderText('must have at least one style')
            result = False
        if self.view.lineedit_set_by.text() == '':
            self.view.lineedit_set_by.setPlaceholderText('must have a setter')
            result = False
        if self.view.lineedit_set_date.text() == '':
            self.view.lineedit_set_date.setPlaceholderText('must have a setting date in YYYY-MM-DD')
            result = False
        return result

    def _make_problem(self):
        try:
            return self._try_make_problem() 
        except ValueError:
            self.view.lineedit_set_date.setText('')
            self.view.lineedit_set_date.setPlaceholderText('expect a date in format YYYY-MM-DD')
            return None

    def _try_make_problem(self):
        
        _id    = int(self.view.text_id.text())
        _r     = int(self.view.dropdown_r.currentText())
        _i     = int(self.view.dropdown_i.currentText())
        _c     = int(self.view.dropdown_c.currentText())
        ric    = RIC(_r,_i,_c)
        grade  = Grade.from_str(self.view.text_grade.text())
        colour = self.view.dropdown_hold.currentText()
        sector = self.view.text_sector.text().lower()
        styles = self._get_styles_tuple()
        set_by = self.view.lineedit_set_by.text()
        set_date = date.fromisoformat(self.view.lineedit_set_date.text())
        status = self.view.dropdown_status.currentText().lower()

        return Problem(_id, ric, grade, colour, sector, styles, set_by, set_date, status)

    def _get_styles_tuple(self):
        _styles = [getattr(self.view, 'lineedit_styles_' + str(index)).text() for index in range(3) ]
        _non_empty_styles = [style for style in _styles if style != '']
        return tuple(_non_empty_styles)

    def _reset_placeholder_texts(self):
        self.view.lineedit_styles_0.setPlaceholderText('')
        self.view.lineedit_set_by.setPlaceholderText('')
        self.view.lineedit_set_date.setPlaceholderText('YYYY-MM-DD')

    def delete_problem(self):
        problem_request = self._dependency.get(ProblemRequest)
        _id = self.view.text_id.text()
        if _id != '':
            _id = int(_id)
            problem_request.delete_problem(_id)
            