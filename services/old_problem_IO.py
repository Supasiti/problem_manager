import json
import os
from collections.abc import Callable

from APImodels.problem import Problem

class OldProblemIO():
    # read old problems from a history folder

    def __init__(self, directory=''):
        self._problems = tuple()
        self._data     = dict()
        self._dir      = self.set_dir(directory) if directory !='' else ''
       
    def set_dir(self, dir_path:str) -> None:
        if not os.path.isdir(dir_path):
            self._dir = ''
        else: 
            self._dir      = dir_path
            self._problems = self._load_problems()

    def _load_problems(self) -> tuple[Problem,...]:
        # getting the last 12 files to view problems - expect about 500 problems in these files
        filepaths = self._get_latest_filepaths(12)
        problems  = []
        for path in filepaths:
            problems.extend(self._load_problems_from_file(path))
        return problems

    def _get_latest_filepaths(self, limit:int) -> list:
        filepaths = self._get_filepaths_from_dir()
        filepaths.sort(reverse=True)
        filepaths = filepaths[0:limit] if len(filepaths) > limit else filepaths
        return filepaths

    def _get_filepaths_from_dir(self) -> list:
        # return list of filepaths
        if os.path.isdir(self._dir):
            filenames = (name for name in os.listdir(self._dir) if name.endswith('.json'))
            return [os.path.join(self._dir, name) for name in filenames]
        return []

    def _load_problems_from_file(self, filepath:str) -> list[Problem,...]:
        # assume that filepath exists
        if os.path.getsize(filepath) == 0:
            return []
        with open(filepath, 'r') as fid:
            data = json.loads(fid.read())
            return [Problem.from_json(p) for p in data.values()]

    def get_all_problems(self) -> tuple[Problem,...]:
        return self._problems

    def filter_problems_by(self, predicate:Callable[[Problem],bool]) -> tuple[Problem,...]:
        return tuple([p for p in self._problems if predicate(p)])
