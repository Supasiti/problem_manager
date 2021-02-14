from services.signal import Signal
from services.path_builder import PathBuilder
from services.repository_factory import RepositoryFactory
from APImodels.problem import Problem

class ProblemRequest():
    # handle all queries about problems
    
    problemToEditChanged = Signal(bool)
    problemsChanged      = Signal(bool)
    _filepath :str

    def __init__(self):
        self._path_builder = PathBuilder()
        self._problems_to_edit = dict()
        self._problem_to_edit  = None
        self._repo_factory = RepositoryFactory()
 
    @property
    def problems(self):
        return self._problems_to_edit.values()
    
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


    def get_problems_from_directory(self, directory:str):
        self._filepath = self._path_builder.get_latest_gym_filepath(directory)   
        if self._filepath != "":
            repository    = self._repo_factory.get(self._filepath)
            self.problems = dict({p.id: p for p in repository.get_all_problems()})


    # def get_all_current_problems(self, directory:str):
    #     self._filepath = self._path_builder.get_latest_gym_filepath(directory)   
    #     if self._filepath != "":
    #         repository    = self._repo_factory.get(self._filepath)
    #         self.problems = dict({p.id: p for p in repository.get_all_problems()})
    #         # return self.problems
    #     return tuple()

    def get_all_sectors(self, directory:str):
        self._filepath = self._path_builder.get_latest_gym_filepath(directory)   
        if self._filepath != "":
            repository    = self._repo_factory.get(self._filepath)
            return repository.get_all_sectors()
        return tuple()

    def get_problem_by_id(self, problem_id:int):
        assert (type(problem_id) == int)
        if self._dict_is_non_empty_and_id_in_keys(problem_id):
            return self._problems_to_edit[problem_id]
        return None

    def _dict_is_non_empty_and_id_in_keys(self, problem_id:int):
        assert (type(problem_id) == int)
        return len(self._problems_to_edit) >0 and problem_id in self._problems_to_edit.keys()

    def get_next_available_problem_id(self):
        return max(self._problems_to_edit.keys()) + 1

    def save_current_problem(self):
        if self._problem_to_edit is None:
            return True
        _id = self._problem_to_edit.id 
        self._problems_to_edit[_id] = self._problem_to_edit
        self._problem_to_edit = None
        return True