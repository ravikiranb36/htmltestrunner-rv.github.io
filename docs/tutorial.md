#Getting Started
##Installation of HTMLTestRunner-rv
```shell
pip install HTMLTestRunner-rv
```
##Importing HTMLTestRunner
```python
from HTMLTestRunner import HTMLTestRunner
```
##Import unittest
```python
import unittest
```
##import your testcase classes
```python
from testcase_file1 import TestCase1
from testcase_file2 import TestCase2
```
##Create suite
```python
test1 = unittest.TestLoader().loadTestsFromTestCase(TestCase1)
test2 = unittest.TestLoader().loadTestsFromTestCase(TestCase2)
suite = unittest.TestSuite([test1, test2])
```
##Create Runner
```python
runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                        open_in_browser=True, description="HTMLTestReport")
```
```python
runner.run(suite)
```
##GOOD LUCK!!