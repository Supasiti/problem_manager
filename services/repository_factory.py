
from services.problem_repository import ProblemRepository

class RepositoryFactory():

    def __init__(self):
        self.filepath = ''
        self.repository = None
    
    def get(self, filepath):
        if filepath != self.filepath or self.repository is None:
            self.filepath = filepath
            self.repository = ProblemRepository(self.filepath)
        return self.repository