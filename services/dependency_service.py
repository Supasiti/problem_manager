# Control all dependencies that controllers will need
from typing import Dict
from threading import Lock
from inspect import signature

# from path_builder import PathBuilder

class DependencyService():
    # very naive dependency registry 
    #  - register only concrete implementation of a class

    _dependencies = Dict[type , object]

    def __init__(self):
        self._dependencies = dict()
        self.padlock = Lock()

    def register(self, class_type: type, dependency:object = None) ->bool:
        
        with self.padlock:
            if class_type in self._dependencies.keys():
                return True
            elif dependency != None:
                self._dependencies[class_type] = dependency
                return True
            elif self._n_non_default_args(class_type) == 0:
                self._dependencies[class_type] = class_type()
                return True
            else:
                raise TypeError('__init__() requires positional arguments')
                
    def get(self, class_type:type) -> object:
        if class_type in self._dependencies.keys():
            return self._dependencies[class_type]
        return None
    
    def get_or_register(self, class_type:type) -> object:
        with self.padlock:
            if not class_type in self._dependencies.keys():
                self._dependencies[class_type] = class_type()    
            return self._dependencies[class_type]


    def deregister(self, class_type:type) -> bool:
        with self.padlock:
            if class_type in self._dependencies.keys():
                self._dependencies.pop(class_type) 
        return True

    def _n_non_default_args(self, class_type:type) ->int:
        sig = signature(class_type)
        non_default_args = [arg for arg in sig.parameters.values() if arg.default is arg.empty]
        return len(non_default_args)