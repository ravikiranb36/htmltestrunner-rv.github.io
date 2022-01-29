# HTMLTestRunner
```text
HTMLTestRunner for python3 

A TestRunner for use with the Python unit testing framework. 
It generates a HTML report to show the result at a glance.
It logs stdout to *.txt file with timestamp
Easy to find bugs
```
#[<span style="color: grey;"> Click here for HTMLTestRunner-rv documentation</span>](https://ravikiranb36.github.io/htmltestrunner-rv.github.io/)

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
    runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                            open_in_browser=True, description="HTMLTestReport")
    runner.run(suite)
if __name__ == '__main__':
test_suite()
```
## Now you can pass external css styling and javascript for report
### Example:
```python
style = """
    .heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
    border-style:ridge;
    color:white;
    background-color:#999900;
    font-weight:bold;
    }
"""
script = """
    Your script
"""
runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                        open_in_browser=True, description="HTMLTestReport", script=script, style=style)
```