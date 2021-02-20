from typing import NamedTuple 


class Colour(NamedTuple):
    
    red   : int
    green : int
    blue  : int 

    def to_tuple(self):
        return (self.red, self.green, self.blue)
    
    @staticmethod
    def from_json(data):
        return Colour(int(data['red']), int(data['green']), int(data['blue']))