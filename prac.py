from services.setting import Setting , GradeSettingParser
from services.file_setting import FileSetting
from services.grade_setting import GradeSetting
import json
from APImodels.colour import Colour
from APImodels.grade import Grade
from services.grade_setting import GradeStyle
from models.dicts import ColourDict, GradeDict



if __name__ == '__main__':
    # setting = Setting()
    # grade_setting = setting.get(GradeSetting)
    # grade_setting.get_data()

    parser = GradeSettingParser()
    setting = parser.get_data()
    print(setting.get_grade(2))


    grade_dict = GradeDict()
    colour_dict = ColourDict()

    styles_to_update = []
    for name in grade_dict.get_all_grades():
        grade = Grade.from_str(name)
        row = grade_dict.get_row(name)
        aim = grade_dict.get_aim(row)
        bg  = Colour( *colour_dict.get_colour(name)[0:3])
        txt = Colour( *colour_dict.get_colour(name)[3:6])
        hover = Colour( *colour_dict.get_colour(name)[6:9])
        
        style = GradeStyle(grade,row,aim,bg,txt,hover) 
        styles_to_update.append(style)
    #     print('"{}":{},'.format(row, json.dumps(style.to_dict(), indent=4, sort_keys=True)))
    # print('}')
    print(len(styles_to_update))

    parser.set_data(styles_to_update)
    parser.write()
    