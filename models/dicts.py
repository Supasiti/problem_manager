
class GradeDict():
    # row , aim

    _grade_dict = {
        'yellow mid'  : (0, 4), 
        'yellow hard' : (1, 1), 
        'blue easy'   : (2, 1), 
        'blue mid'    : (3, 4), 
        'blue hard'   : (4, 1),  
        'purple easy' : (5, 2), 
        'purple mid'  : (6, 4), 
        'purple hard' : (7, 2), 
        'green easy'  : (8, 2), 
        'green mid'   : (9, 6), 
        'green hard'  : (10, 2), 
        'red easy'    : (11, 2),
        'red mid'     : (12, 5),
        'red hard'    : (13, 2),
        'black easy'  : (14, 2),
        'black mid'   : (15, 4),
        'black hard'  : (16, 1),
        'white easy'  : (17, 2),
        'white mid'   : (18, 2),
    }

    
    def get_row(self, name: str):
        if name.lower() in self._grade_dict.keys():
            return self._grade_dict[name][0]
    
    def get_grade(self, row:int):
        keys   = list(self._grade_dict.keys())
        values = list(self._grade_dict.values())
        rows   = [value[0] for value in values]
        if row in rows:
            return keys[rows.index(row)]
        raise IndexError('index is out of range.')
    
    def get_all_grades(self):
        return tuple(self._grade_dict.keys())
        
    def get_aim(self, row:int):
        values = list(self._grade_dict.values())
        rows   = [value[0] for value in values]
        aims   = [value[1] for value in values]
        if row in rows:
            return aims[rows.index(row)]
        raise IndexError('index is out of range.')

    def length(self):
        return len(self._grade_dict)
    

class ColourDict():
    # background colour (R G B), text colour (R G B), hover colour (R G B)

    _colours = {
        'yellow mid'  : (255, 225, 142,   0,   0,   0, 255, 240, 197),
        'yellow hard' : (255, 212,  91,   0,   0,   0, 255, 225, 142),
        'blue easy'   : (154, 186, 242,   0,   0,   0, 194, 213, 247),
        'blue mid'    : ( 98, 148, 232,   0,   0,   0, 154, 186, 242),
        'blue hard'   : ( 53, 109, 210,   0,   0,   0,  98, 148, 232),
        'purple easy' : (171, 157, 208,   0,   0,   0, 212, 204, 230),
        'purple mid'  : (131, 113, 187,   0,   0,   0, 171, 157, 208),
        'purple hard' : ( 92,  69, 157, 240, 240, 240, 131, 113, 187),
        'green easy'  : (173, 209, 158,   0,   0,   0, 212, 231, 205),
        'green mid'   : (136, 188, 114,   0,   0,   0, 173, 209, 158),
        'green hard'  : ( 95, 158,  70,   0,   0,   0, 136, 188, 114),
        'red easy'    : (231, 142, 142,   0,   0,   0, 242, 197, 197),
        'red mid'     : (219,  91,  91,   0,   0,   0, 231, 142, 142),
        'red hard'    : (197,   0,   0, 240, 240, 240, 219,  91,  91),
        'black easy'  : (174, 174, 174,   0,   0,   0, 197, 197, 197),
        'black mid'   : (142, 142, 142,   0,   0,   0, 174, 174, 174),  
        'black hard'  : ( 91,  91,  91,   0,   0,   0, 142, 142, 142),
        'white easy'  : (237, 237, 237,   0,   0,   0, 241, 241, 241),
        'white mid'   : (212, 212, 212,   0,   0,   0, 237, 237, 237),
        'orange'      : (255, 142,   0,   0,   0,   0, 245, 169,  96),
        'default'     : ( 30,  30,  30, 240, 240, 240,  60,  60,  60),
        'setting'     : (231, 142, 142,   0,   0,   0, 231, 142, 142),
        'alert'       : (255,   0 ,  0, 240, 240, 240, 219,  91,  91),
    }

    def get_colour(self, name: str):
        if name.lower() in self._colours.keys():
            return self._colours[name]
    
    def get_hold_colours(self, name: str):
        if name.lower() in self._colours.keys():
            return (name.split(' ')[0], 'orange')
    
    def get_all_colours(self):
        return self._colours.keys()


class SectorDict():

    _sector_dict = {
        'front l' : 0,
        'front r' : 1,
        'mid'     : 2,
        'cave l'  : 3,
        'cave r'  : 4,
        'tower l' : 5,
        'tower'   : 6,
        'tower r' : 7,
        'arch l'  : 8,
        'arch r'  : 9,
        'slab l'  : 10,
        'slab'    : 11,
        'slab r'  : 12,
    }

    def get_col(self, name: str):
        if name.lower() in self._sector_dict.keys():
            return self._sector_dict[name]
        raise ValueError('The sector name does not exist!')
    
    def get_sector(self, col:int):
        keys   = list(self._sector_dict.keys())
        values = list(self._sector_dict.values())
        if col in values:
            return keys[values.index(col)]
        raise IndexError('index is out of range.')

    def get_all_sectors(self):
        return tuple(self._sector_dict.keys())
        
    def length(self):
        return len(self._sector_dict)

