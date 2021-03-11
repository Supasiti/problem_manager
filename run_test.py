import unittest

from tests.test_grade import TestGrade
from tests.test_RIC import TestRIC
from tests.test_problem import TestProblem
from tests.test_dependency_service import TestDependencyService
from tests.test_problem_repository import TestProblemRepository  # involve read file
from tests.test_json_writer import TestJsonWriter                # involve read / write file
from tests.test_signal import TestSignal
from tests.test_setting_parsers import TestFileSettingParser     # involve read file
from tests.test_setting_parsers import TestGradeSettingParser    # involve read file
from tests.test_setting_parsers import TestSectorSettingParser   # involve read file
from tests.test_setting_parsers import TestColourSettingParser   # involve read file
from tests.test_problem_editor import TestProblemEditor
from tests.test_old_problem_IO import TestOldProblemIO           # involve read file
from tests.test_old_problem_viewer import TestOldProblemViewer 
from tests.test_problems_editor_history import TestProblemEditorHistory

if __name__ =='__main__':
    unittest.main()
    