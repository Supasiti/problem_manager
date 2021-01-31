# print('__file__   = %s'   % __file__)
# print('__name__   = %s'   % __name__) 
# print('_package__ = %s\n' % __package__)
# import source.tests.test_RIC

from source.tests import test_RIC
import unittest


if __name__ == ' __main__':
    
    unittest.main()
    test_RIC.TestRIC()