import json
import os

from APImodels.problem import Problem

class JsonWriter():

    def __init__(self):
        self._filepath = ''
        self._problems = tuple()
        self._next_id  = 0
        self._sectors  = dict()

    def set_problems(self, problems:tuple[Problem,...]):
        self._problems = problems
    
    def set_next_id(self, _id:int):
        self._next_id = _id

    def set_filepath(self, filepath:str):
        self._filepath = filepath

    def set_sectors(self, sectors:dict):
        self._sectors = sectors

    def write(self):
        data = self._json_data()
        with open(self._filepath, 'w' ) as fid:
            json.dump(data, fid, indent=4, sort_keys=True)
            fid.truncate()
            fid.close()

    def _json_data(self):
        data = dict()
        data['problems'] = dict({str(p.id): p.to_dict() for p in self._problems})
        data['next_id'] = self._next_id
        data['sectors'] = self._sectors
        return data


class StrippedProblemWriter():
    
    _data : dict
    
    def __init__(self, filepath:str='', problems:tuple[Problem,...]=tuple()):
        self._filepath = filepath
        self._problems = problems

    def set_problems(self, problems:tuple[Problem,...]):
        self._problems = problems

    def set_filepath(self, filepath:str):
        self._filepath = filepath
        self._load(self._filepath)

    def _load(self, filepath:str):
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            self._data = dict()
        else:
            with open(filepath, 'r') as fid:
                self._data = json.loads(fid.read())

    def write(self):
        if len(self._problems) == 0:
            return
        new_data = self._json_data()
        for new_id, new_problem in new_data.items():
            self._data[new_id] = new_problem
        with open(self._filepath, 'w' ) as fid:
            json.dump(self._data, fid, indent=4, sort_keys=True)
            fid.truncate()
            fid.close()

    def _json_data(self):
        return dict({str(p.id): p.to_dict() for p in self._problems})