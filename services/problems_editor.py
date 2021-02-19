from __future__ import annotations
from abc import abstractmethod, ABC

from services.signal import Signal
from services.repository_factory import RepositoryFactory
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

    def __init__(self, state:ProblemsEditorState):
        self.change_to_state(state)
        self._problems_to_edit = dict()    # id (int): problem
        self._problem_to_edit  = None
        self._repo_factory     = RepositoryFactory()
        self.next_id = 1
    
    def change_to_state(self, state:ProblemsEditorState):
        self._state = state
        self._state.context = self
        self.stateChanged.emit(state.name)
    
    @property
    def problems(self):
        return tuple(self._problems_to_edit.values())
    
    @problems.setter
    def problems(self, problems:dict):
        self._problems_to_edit = problems
        self.problemsChanged.emit(True)
        
    @property
    def problem_to_edit(self):
        return self._problem_to_edit
    
    @problem_to_edit.setter
    def problem_to_edit(self, problem:Problem):
        self._problem_to_edit = problem
        self.problemToEditChanged.emit(True)

    def load_problems_from_filepath(self, filepath:str):  
        if filepath != '':
            repository    = self._repo_factory.get(filepath)
            self.problems = dict({p.id: p for p in repository.get_all_problems()})
            self.next_id  = self.next_available_problem_id()
        else:
            self.problems = dict()
        return True

    def next_available_problem_id(self) -> int:
        if len(self._problems_to_edit) > 0: 
            return max(max(self._problems_to_edit.keys()) + 1, self.next_id) 
        return 1

    def get_problem_by_id(self, problem_id:int) -> Problem:
        assert (type(problem_id) == int)
        if self._dict_is_non_empty_and_id_in_keys(problem_id):
            return self._problems_to_edit[problem_id]
        return None

    def _dict_is_non_empty_and_id_in_keys(self, problem_id:int):
        assert (type(problem_id) == int)
        return len(self.problems) >0 and problem_id in self._problems_to_edit.keys()

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