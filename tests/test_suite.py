import unittest
from HTMLTestRunner.runner import HTMLTestRunner
from tests.test_1 import TestCase1
from tests.test_2 import TestCase2
from tests.test_skip import TestSkipped
from tests.test_subtest import TestSubTest
from tests.test_error import TestError

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TestCase1))
    suite.addTest(loader.loadTestsFromTestCase(TestCase2))
    suite.addTest(loader.loadTestsFromTestCase(TestSkipped))
    suite.addTest(loader.loadTestsFromTestCase(TestSubTest))
    suite.addTest(loader.loadTestsFromTestCase(TestError))
    return suite

if __name__ == '__main__':
    runner = HTMLTestRunner(
        log=True, 
        verbosity=2, 
        output='report', 
        title='Test Report Review',
        report_name='report',
        open_in_browser=True,
        description="Testing Skip and SubTest features", 
        tested_by="Ravikirana B"
    )
    runner.run(suite())
