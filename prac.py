from services.setting import Setting , SectorSettingParser
from APImodels.problem import Problem
from APImodels.RIC import RIC
from APImodels.grade import Grade
import datetime
from services.grade_setting import GradeSetting
import json
from APImodels.colour import Colour
from APImodels.grade import Grade

from services.colour_setting import ColourStyle




if __name__ == '__main__':
    # setting = Setting()
    # grade_setting = setting.get(GradeSetting)
    # grade_setting.get_data()

    parser = SectorSettingParser()
    setting = parser.get_data()
    print(setting.get_col('front r'))


    # # grade_dict = GradeDict()
    # colour_dict = ColourDict()

    # # print('{')
    # styles_to_update = []
    # for name in colour_dict.get_all_colours():
    #     name = str(name)
    #     bg    = Colour( *colour_dict.get_colour(name)[0:3])
    #     txt   = Colour( *colour_dict.get_colour(name)[3:6])
    #     hover = Colour( *colour_dict.get_colour(name)[6:9])
        
    #     style = ColourStyle(name,bg,txt,hover) 
    #     styles_to_update.append(style)
    # #     print('"{}":{},'.format(name, json.dumps(style.to_dict(), indent=4, sort_keys=True)))
    # # print('}')
    
    # print(len(styles_to_update))

    # parser.set_data(styles_to_update)
    # parser.write()

    list1 = [1,2,3,4,5,0]
    list1.sort(key= lambda x : int(x))
    list2 = range(6)
    print(list1 == list2)
    res = all(ele >= 0 and ele < 6 for ele in list1)
    print(res)