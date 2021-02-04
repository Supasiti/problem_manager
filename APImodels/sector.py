# Python version 3.9.1
# class containing all the information on each climbing sector

class Sector():

    def __init__(self, name:str):
        self._name = name
        self._problem_ids = set()
    
    def add_problems(self, problem_ids=None):
        if problem_ids is None:
            raise ValueError('Must include at least 1 problem id')
        if isinstance(problem_ids, int):
            self._problem_ids.add(problem_ids)
        if isinstance(problem_ids, (list, tuple, set)):
            _problem_ids = {id for id in problem_ids if isinstance(id, int)}
            self._problem_ids = self._problem_ids.union(_problem_ids)
    
    def contains_problem(self, id: int):
        return id in self._problem_ids

    def remove_problem(self, id: int):
        self._problem_ids.remove(id)

if __name__ == '__main__':
    sector = Sector('Front')
