from services.setting import Setting , SectorSettingParser


from services.grade_setting import GradeSetting
import json
from APImodels.colour import Colour
from APImodels.grade import Grade

from services.colour_setting import ColourStyle
from models.dicts import ColourDict, GradeDict



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

    