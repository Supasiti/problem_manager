# Climbing grade with difficulty within the grade
#  - value class for data transfer
#  - immutable
#  - A grade consists of the range and the difficulty within that range

from typing import NamedTuple

class Grade(NamedTuple):
    range : str
    difficulty :str

    def __str__(self):
        return '%s %s' % (self.range, self.difficulty)

    def __repr__(self):
        return 'Grade(%s, %s)' % (self.range, self.difficulty)

    def to_dict(self):
        return {'range': self.range, 'difficulty':self.difficulty}
        
    @staticmethod
    def from_str(data: str):
        _txt = data.split(' ')
        if len(_txt) != 2: 
            raise ValueError('Incorrect value format. Expected a string of format: "range difficulty"')
        return Grade(_txt[0], _txt[1])
    
    @staticmethod
    def from_json(data):
        return Grade(data['range'], data['difficulty'])