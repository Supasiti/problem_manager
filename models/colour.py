

from collections import namedtuple 

class Colour(namedtuple( 'Colour', ['red', 'green', 'blue'])):
    
    def to_tuple(self):
        return (self.red, self.green, self.blue)
