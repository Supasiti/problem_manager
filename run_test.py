import unittest

from tests.test_grade import TestGrade
from tests.test_RIC import TestRIC
from tests.test_problem import TestProblem
from tests.test_dependency_service import TestDependencyService
from tests.test_problem_repository import TestProblemRepository  # involve read file
from tests.test_json_writer import TestJsonWriter                # involve read / write file
from tests.test_signal import TestSignal
from tests.test_setting_parsers import TestFileSettingParser     # involve read / write file
from tests.test_setting_parsers import TestGradeSettingParser    # involve read / write file
from tests.test_problem_editor import TestProblemEditor

if __name__ =='__main__':
    unittest.main()