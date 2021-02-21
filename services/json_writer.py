import json

from APImodels.problem import Problem

class JsonWriter():

    def __init__(self, filepath:str, problems:tuple[Problem,...]=None, next_id:int=0):
        self._filepath = filepath
        self._problems = problems
        self._next_id  = next_id

    def set_problems(self, problems:tuple[Problem,...]):
        self._problems = problems
    
    def set_next_id(self, _id:int):
        self._next_id = _id

    def write(self):
        data = self._json_data()
        with open(self._filepath, 'w' ) as fid:
            json.dump(data, fid, indent=4, sort_keys=True)
            fid.truncate()
            fid.close()

    def _json_data(self):
        data = {str(p.id): p.to_dict() for p in self._problems}
        data['next_id'] = self._next_id
        return data