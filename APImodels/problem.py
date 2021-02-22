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
        ['id', 'RIC', 'grade', 'colour', 'sector','styles', 'set_by', 'set_date', 'strip_date'],
        defaults = ('', RIC(1,1,1), Grade('yellow','mid'), '','', (), '', None, None)
    )):

    @staticmethod
    def from_json(data):
        _id      = int(data['id'])
        ric      = RIC(int(data['RIC']['R']), int(data['RIC']['I']), int(data['RIC']['C']))
        grade    = Grade.from_json(data['grade'])
        colour   = data['colour']
        sector   = data['sector']
        styles   = tuple(data['styles'])
        set_by   = data['set_by']
        set_date = date.fromisoformat(data['set_date'])
        strip_date = None if data['strip_date'] == None else date.fromisoformat(data['strip_date'])

        return Problem(_id, ric, grade, colour, sector, styles, set_by, set_date, strip_date)
              
    
    def to_dict(self):
        result = {
            'id'       : self.id,
            'RIC'      : self.RIC.to_dict(),
            'grade'    : self.grade._asdict(),
            'colour'   : self.colour,
            'sector'   : self.sector,
            'styles'   : self.styles,
            'set_by'   : self.set_by,
            'set_date' : self.set_date.isoformat(),
            'strip_date' : None if self.strip_date == None else self.strip_date.isoformat()
        }
        return result
    
    def with_strip_date(self, new_date:date):
        _id      = self.id
        ric      = self.RIC
        grade    = self.grade
        colour   = self.colour
        sector   = self.sector
        styles   = self.styles
        set_by   = self.set_by
        set_date = self.set_date
        strip_date = new_date
        
        return Problem(_id, ric, grade, colour, sector, styles, set_by, set_date, strip_date)