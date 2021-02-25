from datetime import date

from services.dependency_service import DependencyService
from services.problems_editor import ProblemsEditor
from services.setting import Setting
from services.colour_setting import ColourSetting
from models.editor_model import EditorModel, EditorData 
from views.editor_view import EditorView
from APImodels.problem import Problem, ProblemEditingType
from APImodels.RIC import RIC
from APImodels.grade import Grade

class EditorController():
    # controller all interaction the problem editor view 
    
    _editor         : ProblemsEditor
    _colour_setting : ColourSetting
    _setting        : Setting

    def __init__(self, dependency: DependencyService):
        self._setup_dependencies(dependency)
        self._view_mode    = False
        self.model         = EditorModel(dynamic_data = self.view_data()) # load model
        self.view          = EditorView(self, self.model)  # load view
        self._connect_other()

    def _setup_dependencies(self, dependency:DependencyService):
        self._dependency     = dependency
        self._editor         = self._dependency.get(ProblemsEditor)
        self._setting        = self._dependency.get(Setting)
        self._colour_setting = self._setting.get(ColourSetting)

    def _connect_other(self):
        self._editor.problemTypeChanged.connect(self._on_problem_type_changed)
        self._editor.stateChanged.connect(self._on_state_changed)

    def _on_problem_type_changed(self, arg:ProblemEditingType) ->bool:
        problem = self._editor.problem_to_edit
        if self._view_mode:
            self.model.dynamic_data = self.view_data(problem=problem)
        else:
            self.model.dynamic_data = self.view_data(problem=problem, problemType=arg)

    def view_data(self, problem:Problem = None, problemType:ProblemEditingType = ProblemEditingType()):
        _problem  = Problem() if problem is None else problem
        holds     = self._colour_setting.get_hold_colours(_problem.grade)
        return EditorData(holds, _problem, problemType.is_strippable, problemType.is_deletable, problemType.is_addable)

    def _on_state_changed(self, name:str):
        self._view_mode = True if name == 'viewing' else False
        self.model.dynamic_data = self.view_data()

    def update_problem(self):
        # assume that buttons only offer all the actions available
        _selected  = self._cell_selected()
        _completed = self._form_is_completed()
        _problem   = self._make_problem() if _selected and _completed else None
 
        if not _problem is None: 
            self._editor.add_new_problem(_problem)
            self._reset_placeholder_texts()

    def _cell_selected(self):
        return self.view.text_id.text() != '' and self.view.text_sector.text() !=  '' 
        
    def _form_is_completed(self):
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
        self.view.lineedit_strip_date.setPlaceholderText('YYYY-MM-DD')

    def delete_problem(self):
        # assume that buttons only offer all the actions available
        _id    = self.view.text_id.text()
        if _id != '':
            _id = int(_id)
            self._editor.delete_problem(_id)

    def strip_problem(self) -> None:
        # strip the problem : need to check if strip date have been filled
        if not self._strip_date_is_completed(): return
        
        strip_date = self._try_parse_date()
        _id        = self.view.text_id.text()
        if _id != '':
            _id   = int(_id)
            self._editor.strip_problem(_id, strip_date)
            self._reset_placeholder_texts()
            self.view.lineedit_strip_date.setText('')

    def _strip_date_is_completed(self) -> bool:
        if  self.view.lineedit_strip_date.text()== '':
            self.view.lineedit_strip_date.setPlaceholderText('must have a strip date in YYYY-MM-DD')
            return False
        return True

    def _try_parse_date(self) -> date:
        try:
            return date.fromisoformat(self.view.lineedit_strip_date.text())
        except ValueError:
            self.view.lineedit_strip_date.setText('')
            self.view.lineedit_strip_date.setPlaceholderText('expect a date in format YYYY-MM-DD')