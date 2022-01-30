import unittest
import math

from HTMLTestRunner.runner import HTMLTestRunner
from tests.test_1 import TestCase1
from tests.test_2 import TestCase2

test1 = unittest.TestLoader().loadTestsFromTestCase(TestCase1)
test2 = unittest.TestLoader().loadTestsFromTestCase(TestCase2)
suite = unittest.TestSuite([test1, test2])
runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                        open_in_browser=True, description="HTMLTestReport")

runner.run(suite)

