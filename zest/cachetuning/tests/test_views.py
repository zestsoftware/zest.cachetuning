import unittest
from Testing import ZopeTestCase as ztc

from zest.cachetuning.tests.base import TestCase

def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
           'views.txt', package='zest.cachetuning.tests',
           test_class=TestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
