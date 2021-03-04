# from tests.test_problem_editor import MockRepository
# from datetime import date

from services.setting import Setting
from services.file_setting import FileSetting
if __name__ == '__main__':


    file_setting = Setting.get(FileSetting)
    print(type(file_setting))