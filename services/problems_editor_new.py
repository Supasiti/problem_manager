from __future__ import annotations
from abc import abstractmethod, ABC

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
    
    _repository : ProblemRepository
    _next_id    : int

    def __init__(self, state:ProblemsEditorState):
        self.change_to_state(state)
        self._problems_init      = dict()  # id (int): problem
        self._problems_to_add    = dict()  # id (int): problem
        self._problems_to_strip  = dict()  # id (int): problem
        self._problem_to_edit  = None

    
    def change_to_state(self, state:ProblemsEditorState):
        self._state = state
        self._state.context = self
        self.stateChanged.emit(state.name)
    
    @property
    def problems(self):
        return tuple(self._problems_to_init.values())
    
    @problems.setter
    def problems(self, problems:dict):
        self._problems_to_init = problems
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
    
    def set_repository(self, value:ProblemRepository):
        self._repository = value

    def load_problems(self) -> bool:  
        if not self._repository is None:
            self.problems = dict({p.id: p for p in self._repository.get_all_problems()})
            self.next_id  = self._repository.next_id
        else:
            self.problems = dict()
            self.next_id  = 0
        return True

    def next_available_problem_id(self) -> int:
        ids = self._problems_init.keys() + self._problems_to_add.keys() + self._problems_to_strip.keys()
        if len(ids) > 0: 
            return max(max(ids) + 1, self.next_id) 
        return 0

    def get_problem_by_id(self, problem_id:int) -> Problem:
        # find id in problems_init or problems_to_add
        assert (type(problem_id) == int)
        if problem_id in self._problems_init.keys():
            return self._problems_init[problem_id]
        if problem_id in self._problems_to_add.keys():
            return self._problems_to_add[problem_id]
        return None

    # TODO 
    # --------------------------
    def save_new_problem(self, problem:Problem) -> bool:
        assert (type(problem) == Problem)
        self._state.save_new_problem(problem, self._problems_to_edit)

    def delete_problem(self, problem_id:int) -> bool:
        assert(type(problem_id)==int)
        return self._state.delete_problem(problem_id, self._problems_to_edit)
    
    def save_this_set(self, filepath:str):
        self._state.save_this_set(filepath)

    def save_as_new_set(self, filepath:str):
        self._state.save_as_new_set(filepath)


class ProblemsEditorState(ABC):

    _context     : ProblemsEditor

    @property
    def context(self) -> ProblemsEditor:
        return self._context

    @context.setter
    def context(self, context: ProblemsEditor) -> None:
        self._context = context

    @abstractmethod
    def save_new_problem(self, problem:Problem, problems: dict[Problem,...]) -> bool:
        pass

    @abstractmethod
    def delete_problem(self, problem_id:int, problems: dict[Problem,...]) -> bool:
        pass

    @abstractmethod
    def save_this_set(self, filepath:str):
        pass

    @abstractmethod
    def save_as_new_set(self, filepath:str):
        pass


class EditingProblemsEditor(ProblemsEditorState):
    # can edit the problems

    def __init__(self):
        super().__init__()
        self.name = 'editing'
    
    def save_new_problem(self, problem:Problem, problems: dict[Problem,...]) -> bool:
        _id = int(problem.id) 
        problems[_id] = problem
        self._context.problemAdded.emit(problem)
        self._context.problem_to_edit = None
        self._context.next_id = self._context.next_available_problem_id()
        return True

    def delete_problem(self, problem_id:int, problems: dict[Problem,...]) -> bool:
        if problem_id in problems.keys():
            to_remove = problems.pop(problem_id)
            self._context.problemRemoved.emit(to_remove)
        self._context.problem_to_edit = None
        return True

    def save_this_set(self, filepath:str):
        # update the current file with new data
        # assume path is already been verified
        writer   = JsonWriter(filepath, self._context.problems)
        writer.write()

    def save_as_new_set(self, filepath:str):
        # assume path is already been verified
        writer   = JsonWriter(filepath, self._context.problems)
        writer.write()


class ViewingProblemsEditor(ProblemsEditorState):
    # can only view problems

    def __init__(self):
        super().__init__()
        self.name = 'viewing'

    def save_new_problem(self, problem:Problem, problems: dict[Problem,...]) -> bool:
        return True

    def delete_problem(self, problem_id:int, problems: dict[Problem,...]) -> bool:
        return True

    def save_this_set(self, filepath:str):
        pass

    def save_as_new_set(self, filepath:str):
        pass