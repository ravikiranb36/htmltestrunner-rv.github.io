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

from HTMLTestRunner.runner import HTMLTestRunner
from tests.test_1 import TestCase1
from tests.test_2 import TestCase2

test1 = unittest.TestLoader().loadTestsFromTestCase(TestCase1)
test2 = unittest.TestLoader().loadTestsFromTestCase(TestCase2)
suite = unittest.TestSuite([test1, test2])
runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                        open_in_browser=True, description="HTMLTestReport", tested_by="Ravikirana B",
                        add_traceback=False)

runner.run(suite)
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