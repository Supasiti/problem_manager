import json
import os

from services.path_builder import PathBuilder
from APImodels.problem import Problem

class ProblemRequest():
    # handle all queries about problems
    
    filepath :str

    def __init__(self):
        self.path_builder = PathBuilder()

    def get_all_current_problems(self, directory:str):
        
        self.filepath = self.path_builder.get_latest_gym_filepath(directory)
   
        # parse the data
        with open(self.filepath, 'r') as fid:
            data = json.loads(fid.read())
            result = [Problem.from_json(p) for p in data ]
        return result