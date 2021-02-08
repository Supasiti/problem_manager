# Climbing grade with difficulty within the grade
#  - value class for data transfer
#  - immutable
#  - A grade consists of the range and the difficulity within that range

from typing import NamedTuple

class Grade():

    _accepted_ranges = ('yellow','blue','purple','green','red','black','white')
    _accepted_difficulties = ('easy','mid','hard')
    _range: str
    _difficulty:str

    def __init__(self, grade:str, difficulty:str):
        self.validate('_range', grade, self._accepted_ranges)
        self.validate('_difficulty', difficulty, self._accepted_difficulties)

    @property
    def range(self):
        return self._range

    @property
    def difficulty (self):
        return self._difficulty

    def validate(self, tag: str, value:str, accepted_values:tuple):
        lowercase = value.lower()
        if lowercase not in accepted_values:
            raise ValueError('%s is not one of %s' % (value, accepted_values))
        setattr(self, tag, lowercase)

    def __str__(self):
        return '%s %s' % (self.range, self.difficulty)

    def __repr__(self):
        return 'Grade(%s, %s)' % (self.range, self.difficulty)

