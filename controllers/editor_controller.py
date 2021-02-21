from datetime import date

from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from services.setting import Setting
from services.colour_setting import ColourSetting
from models.editor_model import EditorModel, EditorData 
from views.editor_view import EditorView
from APImodels.problem import Problem
from APImodels.RIC import RIC
from APImodels.grade import Grade

class EditorController():
    # controller all interaction the problem editor view 
    
    _editor         : ProblemsEditor
    _colour_setting : ColourSetting
    _setting        : Setting

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        self._is_updatable = True
        self.model         = EditorModel(dynamic_data = self.view_data()) # load model
        self.view          = EditorView(self, self.model)  # load view
        self._connect_other()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)
        self._setting        = self._dependency.get(Setting)
        self._colour_setting = self._setting.get(ColourSetting)

    def _connect_other(self):
        self._editor.problemToEditChanged.connect(self._on_problem_to_edit_changed)
        self._editor.stateChanged.connect(self._on_state_changed)

    def _on_problem_to_edit_changed(self, arg:bool):
        self.model.dynamic_data = self.view_data(self._editor.problem_to_edit)
        return True

    def view_data(self, problem:Problem = None):
        _problem  = Problem() if problem is None else problem
        holds     = self._colour_setting.get_hold_colours(_problem.grade)
        return EditorData(holds, _problem, self._is_updatable)

    def _on_state_changed(self, name:str):
        if name == 'editing':
            self._is_updatable = True
        elif name == 'viewing':
            self._is_updatable = False
        else:
            raise ValueError('incorrect state')
        self.model.dynamic_data = self.view_data()

    def update_problem(self):
        _is_updatable = True
        _is_updatable = self._cell_selected()
        _is_updatable = self._prompt_if_form_incomplete()
        _problem      = self._make_problem() if _is_updatable else None
 
        if not _problem is None: 
            self._editor.save_new_problem(_problem)
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
        strip_date = None

        return Problem(_id, ric, grade, colour, sector, styles, set_by, set_date, strip_date)

    def _get_styles_tuple(self):
        _styles = [getattr(self.view, 'lineedit_styles_' + str(index)).text() for index in range(3) ]
        _non_empty_styles = [style for style in _styles if style != '']
        return tuple(_non_empty_styles)

    def _reset_placeholder_texts(self):
        self.view.lineedit_styles_0.setPlaceholderText('')
        self.view.lineedit_set_by.setPlaceholderText('')
        self.view.lineedit_set_date.setPlaceholderText('YYYY-MM-DD')

    def delete_problem(self):
        _id    = self.view.text_id.text()
        if _id != '':
            _id = int(_id)
            self._editor.delete_problem(_id)
