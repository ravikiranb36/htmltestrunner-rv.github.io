import unittest

from HTMLTestRunner.runner import HTMLTestRunner
from tests.test_1 import TestCase1
from tests.test_2 import TestCase2
from tests.test_skip import TestSkipped

test1 = unittest.TestLoader().loadTestsFromTestCase(TestCase1)
test2 = unittest.TestLoader().loadTestsFromTestCase(TestCase2)
test3 = unittest.TestLoader().loadTestsFromTestCase(TestSkipped)
suite = unittest.TestSuite([test1, test2, test3])
runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                        open_in_browser=True, description="HTMLTestReport", tested_by="Ravikirana B",
                        add_traceback=False)

runner.run(suite)
