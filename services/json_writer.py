import json

from APImodels.problem import Problem

class JsonWriter():

    def __init__(self, filepath:str, problems:tuple[Problem,...]=None):
        self._filepath = filepath
        self._problems = problems

    def set_problems(self, problems:tuple[Problem,...]):
        self._problems = problems

    def write(self):
        data = self._json_data()
        with open(self._filepath, 'w' ) as fid:
            json.dump(data, fid, indent=4, sort_keys=True)
            fid.truncate()
            fid.close()

    def _json_data(self):
        return list([p.to_dict() for p in self._problems])