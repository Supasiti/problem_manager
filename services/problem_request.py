
from services.path_builder import PathBuilder
from services.repository_factory import RepositoryFactory

class ProblemRequest():
    # handle all queries about problems
    
    filepath :str

    def __init__(self):
        self.path_builder = PathBuilder()
        self.repo_factory = RepositoryFactory()

    def get_all_current_problems(self, directory:str):
        
        self.filepath = self.path_builder.get_latest_gym_filepath(directory)   
        repository    = self.repo_factory.get(self.filepath)
        return repository.get_all_problems()
