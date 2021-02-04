
class GradeDict():

    __grade_dict = {
        'yellow mid'  : 0,  
        'yellow hard' : 1,  
        'blue easy'   : 2,  
        'blue mid'    : 3,  
        'blue hard'   : 4,   
        'purple easy' : 5,  
        'purple mid'  : 6,  
        'purple hard' : 7,  
        'green easy'  : 8,  
        'green mid'   : 9,  
        'green hard'  : 10, 
        'red easy'    : 11, 
        'red mid'     : 12, 
        'red hard'    : 13, 
        'black easy'  : 14, 
        'black mid'   : 15, 
        'black hard'  : 16, 
        'white easy'  : 17, 
        'white mid'   : 18
    }

    
    def get_row(self, name: str):
        if name.lower() in self.__grade_dict.keys():
            return self.__grade_dict[name]
    
    def length(self):
        return len(self.__grade_dict)
    

class ColourDict():
    # background colour (R G B), text colour (R G B), hover colour (R G B)

    __colours = {
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
        'setting'     : (231, 142, 142,   0,   0,   0, 231, 142, 142)
    }

    def get_colours(self, name: str):
        if name.lower() in self.__colours.keys():
            return self.__colours[name]


class SectorDict():

    __sector_dict = {
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
        if name.lower() in self.__sector_dict.keys():
            return self.__sector_dict[name]

    def length(self):
        return len(self.__sector_dict)