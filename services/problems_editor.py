from abc import abstractmethod, ABC

from services.signal import Signal
from services.repository_factory import RepositoryFactory
from services.json_writer import JsonWriter
from APImodels.problem import Problem

class ProblemsEditor():
    # handle all problems editing 
       
    problemToEditChanged = Signal(bool)
    problemsChanged      = Signal(bool)
    problemAdded         = Signal(Problem)
    problemRemoved       = Signal(Problem)

    def __init__(self):
        # self._state            = None
        self._problems_to_edit = dict()    # id (int): problem
        self._problem_to_edit  = None
        self._repo_factory     = RepositoryFactory()
        self.next_id = 1
 
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

    # def change_state(self):
    #     pass

    def load_problems_from_filepath(self, filepath:str):  
        if filepath != '':
            repository    = self._repo_factory.get(filepath)
            self.problems = dict({p.id: p for p in repository.get_all_problems()})
            self.next_id  = self._next_available_problem_id()
        return True

    def _next_available_problem_id(self) -> int:
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
        _id = int(problem.id) 
        self._problems_to_edit[_id] = problem
        self.problemAdded.emit(problem)
        self.problem_to_edit = None
        self.next_id = self._next_available_problem_id()
        return True

    def delete_problem(self, problem_id:int) -> bool:
        assert(type(problem_id)==int)
        if problem_id in self._problems_to_edit.keys():
            to_remove = self._problems_to_edit.pop(problem_id)
            self.problemRemoved.emit(to_remove)
        self.problem_to_edit = None
        return True
    
    def save_this_set(self, filepath:str):
        # update the current file with new data
        # assume path is already been verified
        writer   = JsonWriter(filepath, self.problems)
        writer.write()

    def save_as_new_set(self, filepath:str):
        # assume path is already been verified
        writer   = JsonWriter(filepath, self.problems)
        writer.write()


# class State(ABC):

#     _context : ProblemsEditor

#     @property
#     def context(self) -> ProblemsEditor:
#         return self._context

#     @context.setter
#     def context(self, context: ProblemsEditor) -> None:
#         self._context = context

#     @abstractmethod
#     def save_new_problem(self, problem:Problem) -> bool:
#         pass

#     @abstractmethod
#     def delete_problem(self, problem_id:int) -> bool:
#         pass

#     @abstractmethod
#     def save_this_set(self):
#         pass

#     @abstractmethod
#     def save_as_new_set(self):
#         pass

    

# class EditingState(State):


#     def save_new_problem(self, problem:Problem) -> bool:
#         assert (type(problem) == Problem)
#         _id = int(problem.id) 
#         self._context.problems_to_edit[_id] = problem
#         self._context.problemAdded.emit(problem)
#         self._context.problem_to_edit = None
#         self._context.next_id = self._context.next_available_problem_id()
#         return True

#     def delete_problem(self, problem_id:int) -> bool:
#         assert(type(problem_id)==int)
#         if problem_id in self._context.problems_to_edit.keys():
#             to_remove = self._context.problems_to_edit.pop(problem_id)
#             self._context.problemRemoved.emit(to_remove)
#         self.problem_to_edit = None
#         return True
    
#     def save_this_set(self):
#         # update the current file with new data
#         writer   = JsonWriter(self.filepath, self.problems)
#         writer.write()

#     def save_as_new_set(self):
#         filepath = self._path_builder.new_gym_filepath(self._directory, self.filename_to_save)
#         writer   = JsonWriter(filepath, self.problems)
#         writer.write()