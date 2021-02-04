# Python version 3.9.1
# Data object containing all the information each problem
#  - immutable

from collections import namedtuple 
from datetime import date
from APImodels.RIC import RIC
from APImodels.grade import Grade

class Problem(
    namedtuple(
        'Problem',
        ['id', 'RIC', 'grade', 'colour', 'sector','styles', 'set_by', 'set_date', 'status'],
        defaults = (-1, RIC(1,1,1), Grade('yellow','mid'), 'yellow','front l', [], '', date.today(), 'on')
    )):

    @staticmethod
    def from_json(data):
        _id      = data['id']
        ric      = RIC(data['RIC']['R'], data['RIC']['I'], data['RIC']['C'])
        grade    = Grade(data['grade']['range'], data['grade']['difficulty'])
        colour   = data['colour']
        sector   = data['sector']
        styles   = data['styles']
        set_by   = data['set_by']
        set_date = date.fromisoformat(data['set_date'])
        status   = data['status']

        return Problem(_id, ric, grade, colour, sector, styles, set_by, set_date, status)
              
        