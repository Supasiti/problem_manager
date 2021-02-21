import unittest
import os

from services.setting import FileSettingParser, GradeSettingParser
from services.file_setting import FileSetting
from services.grade_setting import GradeSetting, GradeStyle
from APImodels.grade import Grade
from APImodels.colour import Colour

class TestSettingParser(unittest.TestCase):

    def create_filepath(cls, folder:str, filename:str):
        real_path = os.path.realpath(__file__)
        dir_path  = os.path.dirname(real_path)
        return os.path.join(dir_path, folder,filename)


class TestFileSettingParser(TestSettingParser):
    # write method is a general method import from json 

    def setUp(self):
        self.data_path  = self.create_filepath('data',     'test_file_setting_data.json')
        self.parser     = FileSettingParser()
        self.parser.set_filepath(self.data_path)

    def test_get_data(self):
        result = self.parser.get_data()

        self.assertEqual(type(result) , FileSetting)
        self.assertEqual(result.content_path, "Contents")

    def test_set_data(self):
        self.parser.set_data('yum yum')
        result = self.parser.get_data()

        self.assertEqual(result.content_path, "yum yum")


class TestGradeSettingParser(TestSettingParser):
    # write method is a general method import from json 

    def setUp(self):
        self.data_path  = self.create_filepath('data', 'test_grade_setting_data.json')
        self.parser     = GradeSettingParser()
        self.parser.set_filepath(self.data_path)
    
    def test_get_data(self):
        result = self.parser.get_data()
        grades = result.get_all_grades()
        
        self.assertEqual(type(result) , GradeSetting)
        self.assertEqual(type(grades[0]) , Grade)
        self.assertEqual(result.length() , 6)

    def test_set_single_data(self):
        # when set_data, it is expected to check for duplicates, and get rid of them.
        # and then set the new data
        #  - style saved to row "6" 
        #  - style to row "0" is deleted due to duplication

        style = GradeStyle(Grade('yellow','mid'), 6, 3, Colour(0,1,2),Colour(3,4,5),Colour(6,7,8) )
        self.parser.set_data(style)
        setting = self.parser.get_data()
        aim     = setting.get_aim(6) 
        
        self.assertEqual(aim , 3)
        with self.assertRaises(IndexError):
            setting.get_row(0)
