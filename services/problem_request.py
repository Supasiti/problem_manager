import json
import os
from datetime import date
from APImodels.RIC import RIC
from APImodels.grade import Grade
from APImodels.problem import Problem

class ProblemRequest():
    # handle all queries about problems

    

    def get_all_current_problems(self, directory:str):
        # return a tuple of all problems in the gym from a particular directory

        result = []
        # get the actual directory
        current_problem_dir = os.path.join(directory, 'current')
     
        # scan the directory and get the most recent one 
        json_files = [path for path in os.listdir(current_problem_dir) if path.endswith('.json')]
        json_files.sort(reverse=True)
        latest_file = json_files[0]
 
        filepath = os.path.join(current_problem_dir, latest_file)
        

        # parse the data
        with open(filepath, 'r') as fid:
            data = json.loads(fid.read())
            
            for problem in data:
                _id      = problem['id']
                ric      = RIC(problem['RIC']['R'], problem['RIC']['I'], problem['RIC']['C'])
                grade    = Grade(problem['grade']['range'], problem['grade']['difficulty'])
                colour   = problem['colour']
                sector   = problem['sector']
                styles   = problem['styles']
                set_by   = problem['set_by']
                set_date = date.fromisoformat(problem['set_date'])
                status   = problem['status']

                problem = Problem(_id, ric, grade, colour, sector, styles, set_by, set_date, status)
                result.append(problem)
        return result