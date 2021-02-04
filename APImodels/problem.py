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
    pass

if __name__ == '__main__':
    prob = Problem(1,RIC(1,2,3),Grade('yellow','hard'),styles=['pop'],set_by='Thara')
    print(prob)