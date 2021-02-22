from __future__ import annotations
from abc import abstractmethod, ABC
from datetime import date

from services.signal import Signal
from services.problem_repository import ProblemRepository
from services.json_writer import JsonWriter
from APImodels.problem import Problem


class ProblemsEditor():
    # handle all problems editing 

    stateChanged         = Signal(str)
    problemToEditChanged = Signal(bool)
    problemsChanged      = Signal(bool)
    problemAdded         = Signal(Problem)
    problemRemoved       = Signal(Problem)
    _state = None
    _next_id    : int

    def __init__(self, state:ProblemsEditorState):
        self.change_to_state(state)
        self._problems_init      = dict()  # id (int): problem : problems already on the wall
        self._problems_to_add    = dict()  # id (int): problem : problems being set
        self._problems_to_strip  = dict()  # id (int): problem : problems being stripped
        self._problem_to_edit    = None

    def change_to_state(self, state:ProblemsEditorState):
        self._state = state
        self._state.context = self
        self.stateChanged.emit(state.name)
    
    @property
    def problems(self):
        problems_on_screen = list(self._problems_init.values()) + list(self._problems_to_add.values())
        return tuple(problems_on_screen)
    
    @problems.setter
    def problems(self, problems:dict):
        self._problems_init = problems
        self._problems_to_add.clear()
        self._problems_to_strip.clear()
        self.problemsChanged.emit(True)
        
    @property
    def problem_to_edit(self):
        return self._problem_to_edit
    
    @problem_to_edit.setter
    def problem_to_edit(self, problem:Problem):
        self._problem_to_edit = problem
        self.problemToEditChanged.emit(True)

    @property
    def next_id(self):
        return self._next_id
    
    @next_id.setter
    def next_id(self, value):
        self._next_id = value
    
    def load_problems(self, repository:ProblemRepository) -> bool:  
        self.problems = dict({p.id: p for p in repository.get_all_problems()})
        self._next_id = repository.next_id
        return True

    def next_available_problem_id(self) -> int:
        ids = list(self._problems_init.keys())  + \
            list(self._problems_to_add.keys()) + \
            list(self._problems_to_strip.keys())
        return max(max(ids) + 1, self.next_id) 
 

    def get_problem_by_id(self, problem_id:int) -> Problem:
        # find id in problems_init or problems_to_add
        assert (type(problem_id) == int)
        if problem_id in self._problems_init.keys():
            return self._problems_init[problem_id]
        if problem_id in self._problems_to_add.keys():
            return self._problems_to_add[problem_id]
        return None

    def add_new_problem(self, problem:Problem,) -> bool:
        assert (type(problem) == Problem)
        self._state.add_new_problem(problem, self._problems_init, self._problems_to_add)

    def delete_problem(self, problem_id:int) -> bool:
        # delete a problem when make a mistake. 
        # doesn't allow to delete saved problem
        assert(type(problem_id)==int)
        return self._state.delete_problem(problem_id, self._problems_to_add)
    
    def strip_problem(self, problem_id:int, strip_date:date) ->bool:
        return self._state.strip_problem(problem_id, strip_date, self._problems_init, self._problems_to_strip)

    def save_this_set(self, writer:JsonWriter):
        self._state.save_this_set(writer)



class ProblemsEditorState(ABC):

    _context     : ProblemsEditor

    @property
    def context(self) -> ProblemsEditor:
        return self._context

    @context.setter
    def context(self, context: ProblemsEditor) -> None:
        self._context = context

    @abstractmethod
    def add_new_problem(self, problem:Problem,  problems: dict[Problem,...], add_to:dict[Problem,...]) -> bool:
        pass

    @abstractmethod
    def delete_problem(self, problem_id:int, problems: dict[Problem,...]) -> bool:
        pass

    @abstractmethod
    def strip_problem(self, problem_id:int, strip_date:date, problems: dict[Problem,...], strip_to:dict[Problem,...]) ->bool:
        pass

    @abstractmethod
    def save_this_set(self, writer:JsonWriter):
        pass


class EditingProblemsEditor(ProblemsEditorState):
    # can edit the problems

    def __init__(self):
        super().__init__()
        self.name = 'editing'
    
    def add_new_problem(self, problem:Problem, problems: dict[Problem,...], add_to:dict[Problem,...]) -> bool:
        # Can only add a problem with either existing ids or next_id
        self._try_add_new_problem(problem, problems, add_to)
        self._context.problemAdded.emit(problem)
        self._context.problem_to_edit = None
        self._context.next_id = self._context.next_available_problem_id()
        return True
    
    def _try_add_new_problem(self, problem:Problem, problems: dict[Problem,...], add_to:dict[Problem,...]) ->None:
        _id = problem.id 
        if _id == self._context.next_id:
            add_to[_id] = problem
        elif _id in problems.keys():
            problems[_id] = problem
        else:
            raise ValueError('trying to add problem with incorrect id!')

    def delete_problem(self, problem_id:int, problems: dict[Problem,...]) -> bool:
        # not to be confused with strip problem - 
        if problem_id in problems.keys():
            to_remove = problems.pop(problem_id)
            self._context.problemRemoved.emit(to_remove)
        self._context.problem_to_edit = None
        return True

    def strip_problem(self, problem_id:int, strip_date:date, problems: dict[Problem,...], strip_to:dict[Problem,...]) ->bool:
        # can only strip the problem already on the wall
        if problem_id in problems.keys():
            prob = problems.pop(problem_id)
            strip_to[problem_id] = prob.with_strip_date(strip_date)
            return True
        else:
            raise IndexError('Problem to be stripped is not found.')

    def save_this_set(self, writer:JsonWriter):
        # update the current file with new data
        # assume path is already been verified
        writer.set_problems(self._context.problems)
        writer.set_next_id(self._context.next_id)
        writer.write()


class ViewingProblemsEditor(ProblemsEditorState):
    # can only view problems

    def __init__(self):
        super().__init__()
        self.name = 'viewing'

    def add_new_problem(self, problem:Problem, problems: dict[Problem,...], add_to:dict[Problem,...]) -> bool:
        return True

    def delete_problem(self, problem_id:int, problems: dict[Problem,...]) -> bool:
        return True

    def strip_problem(self, problem_id:int, strip_date:date, problems: dict[Problem,...], strip_to:dict[Problem,...]) ->bool:
        return True

    def save_this_set(self, writer:JsonWriter):
        pass

