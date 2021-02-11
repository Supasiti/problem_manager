# tests for Dependency Service

import unittest
from services.dependency_service import DependencyService
from services.path_builder import PathBuilder
from services.problem_request import ProblemRequest

class TestDependencyService(unittest.TestCase):

    def setUp(self):
        self.service = DependencyService()

    def test_register(self):
        self.service.register(PathBuilder)
        result = self.service.get(PathBuilder)

        self.assertEqual(len(self.service.dependency_dict), 1)
        self.assertEqual(result.__class__, PathBuilder)
    
    def test_register_instance(self):
        self.service.register(PathBuilder, PathBuilder())
        result = self.service.get(PathBuilder)

        self.assertEqual(len(self.service.dependency_dict), 1)
        self.assertEqual(result.__class__, PathBuilder)
    
    def test_register_twice(self):
        self.service.register(PathBuilder)
        self.service.register(PathBuilder)
        result = self.service.get(PathBuilder)

        self.assertEqual(len(self.service.dependency_dict), 1)
        self.assertEqual(result.__class__, PathBuilder)
    
    def test_get_none(self):
        result = self.service.get(PathBuilder)

        self.assertEqual(result, None)
    
    def test_register_classes(self):
        self.service.register(PathBuilder)
        self.service.register(ProblemRequest)
        result = self.service.get(PathBuilder)

        self.assertEqual(len(self.service.dependency_dict), 2)
        self.assertEqual(result.__class__, PathBuilder)
    
    def test_get_or_register(self):
        result = self.service.get_or_register(PathBuilder)
        
        self.assertEqual(len(self.service.dependency_dict), 1)
        self.assertEqual(result.__class__, PathBuilder)