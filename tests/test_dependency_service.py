# tests for Dependency Service

import unittest
from services.dependency_service import DependencyService
from services.contents_path_manager import ContentsPathManager # doesn't require parameter
from services.problems_editor import ProblemsEditor           # requires parameters
from services.repository_factory import RepositoryFactory     # doesn't require parameter

class TestDependencyService(unittest.TestCase):

    def setUp(self):
        self.service = DependencyService()

    def test_register(self):
        self.service.register(ContentsPathManager)
        result = self.service.get(ContentsPathManager)

        self.assertEqual(result.__class__, ContentsPathManager)
    
    def test_register_instance(self):
        self.service.register(ContentsPathManager, ContentsPathManager())
        result = self.service.get(ContentsPathManager)

        self.assertEqual(result.__class__, ContentsPathManager)
    
    def test_register_class_with_non_default_args(self):
        with self.assertRaises(TypeError):
            self.service.register(ProblemsEditor)
    
    def test_register_twice(self):
        self.service.register(ContentsPathManager)
        self.service.register(ContentsPathManager)
        result = self.service.get(ContentsPathManager)

        self.assertEqual(result.__class__, ContentsPathManager)
    
    def test_get_none(self):
        result = self.service.get(ContentsPathManager)

        self.assertEqual(result, None)
    
    def test_register_classes(self):
        self.service.register(ContentsPathManager)
        self.service.register(RepositoryFactory)
        result = self.service.get(ContentsPathManager)

        self.assertEqual(result.__class__, ContentsPathManager)
    
    def test_get_or_register(self):
        result = self.service.get_or_register(ContentsPathManager)
        
        self.assertEqual(result.__class__, ContentsPathManager)

    def test_deregister(self):
        self.service.register(ContentsPathManager)
        self.service.deregister(ContentsPathManager)
        result = self.service.get(ContentsPathManager)

        self.assertEqual(result, None)