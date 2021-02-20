
from services.problem_repository import ProblemRepository

class RepositoryFactory():

    def __init__(self):
        self._filepath = ''
        self._repository = None
    
    def get(self, filepath):
        if filepath != self._filepath or self._repository is None:
            self._filepath   = filepath
            self._repository = ProblemRepository(self._filepath)
        return self._repository