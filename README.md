# HTMLTestRunner
```text
HTMLTestRunner for python unit test

A TestRunner for use with the Python unit testing framework. It generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g. import unittest from HTMLTestRunner.runner import
HTMLTestRunner ... define your tests ... For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.
```
#Installation:
```bash
pip install HTMLTestRunner-rv
```
# Creating suite
```python
my_test_suite = unittest.TestSuite()
```
# output to a file
```python
runner = HTMLTestRunner(
title='My unit test', open_in_browser=True)
```
# run the test
```python
runner.run(my_test_suite)
```
#Example code:
```python
import unittest
from test_print_all_details import TestCasePrintAllDetails
from test_by_id import TestCaseDetailsById
from test_details_by_name import TestCaseDetailsByNmae
from HTMLTestRunner import HTMLTestRunner

def test_suite():
test1 = unittest.TestLoader().loadTestsFromTestCase(TestCasePrintAllDetails)
test2 = unittest.TestLoader().loadTestsFromTestCase(TestCaseDetailsById)
test3 = unittest.TestLoader().loadTestsFromTestCase(TestCaseDetailsByNmae)
suite = unittest.TestSuite([test1,test2,test3])
runner = HTMLTestRunner(title="Test Report", open_in_browser=True)
runner.run(suite)
if __name__ == '__main__':
test_suite()
```