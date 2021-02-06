# Control all dependencies that controllers will need

from services.problem_request import ProblemRequest

class DependencyService():

    def __init__(self):
        self.problem_request = ProblemRequest()