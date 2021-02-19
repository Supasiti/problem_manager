from services.setting import Setting 
from services.file_setting import FileSetting

if __name__ == '__main__':
    setting = Setting()
    file_setting = setting.get(FileSetting)
    print(file_setting.content_path)