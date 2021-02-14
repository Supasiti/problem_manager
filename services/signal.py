

class Signal():

    def __init__(self, class_type:type = None):
        self._type = class_type
        self._receivers = []

    def connect(self, function:callable):
        self._receivers.append(function)

    def emit(self, obj:object = None): 
        if self._type is None:
            assert (obj is None)
            for func in self._receivers:
                func()
            return True
        else:
            assert( type(obj) == self._type)
            for func in self._receivers:
                func(obj)
            return True