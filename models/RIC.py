# Risk, Intensity, Complexity
#  - value class for data transfer
#  - immutable

class RIC():

    _R: int
    _I: int
    _C: int 

    def __init__(self, r, i, c):
        self.validate_value('_R', r)
        self.validate_value('_I', i)
        self.validate_value('_C', c)

    @property
    def R(self):
        return self._R

    @property
    def I (self):
        return self._I
    
    @property
    def C (self):
        return self._C

    def validate_value(self, tag, value):
        if 1 > value or value > 5: 
            raise ValueError('The value must be in between 1 and 5')
        setattr(self, tag, value)

    def __str__(self):
        return '(R: %s, I:%s C:%s )' % (self.R, self.I, self.C)

    def __repr__(self):
        return 'RIC(%s, %s, %s)' % (self.R, self.I, self.C)