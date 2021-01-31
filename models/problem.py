# Python version 3.9.1
# Data object containing all the information each problem
#  - immutable

from collections import namedtuple 
from datetime import date
from RIC import RIC
from grade import Grade

class Problem(
    namedtuple(
        'Problem',
        ['id', 'RIC', 'grade', 'styles', 'set_by', 'set_date', 'status'],
        defaults = (-1, RIC(1,1,1), Grade('yellow','mid'), [], '', date.today(), 'on')
    )):
    pass

if __name__ == '__main__':
    prob = Problem(1,RIC(1,2,3),Grade('yellow','hard'),['pop'],'Thara')
    print(prob)