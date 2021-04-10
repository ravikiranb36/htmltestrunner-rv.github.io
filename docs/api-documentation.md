#HTMLTestRunner-rv
##HTMLTestRunner.runner


### to\_unicode

```python
to_unicode(s)
```

It strings to unicode

**Arguments**:

- `s` _str_ - String to convert to unicode
  

**Returns**:

  It returns unicode

## OutputRedirector Objects
```python
class OutputRedirector(object)
```

Wrapper to redirect stdout or stderr

### \_\_init\_\_
```python
  __init__(fp)
```

Wrapper to redirect stdout or stderr

**Arguments**:

- `fp` _buffer_ - Buffer to store stdout


### write
```python
  write(s)
```

Write to string buffer with timestamp

**Arguments**:

- `s` _str_ - String to write to buffer
  

**Returns**:

  It returns None


### writelines
```python
  writelines(lines)
```

It write number lines to buffer

**Arguments**:

- `lines` _list_ - List of lines to write to buffer
  

**Returns**:


### flush
```python
  flush()
```

It flushes string buffer

**Returns**:


## _TestResult Objects
```python
class _TestResult(TestResult)
```

### \_\_init\_\_
```python
  __init__(verbosity=1, log_file='')
```

It generates test result

**Arguments**:

- `verbosity` _int_ - If ``verbosity > 1`` it logs all details
- `log_file` _file_ - File name to log the ``stdout`` logs


### startTest
```python
 | startTest(test)
```

Start test inherited by unittest TestResult.
It changes stdout buffer to ``self.outputBuffer``

**Arguments**:

  test : Test object to do test
  

**Returns**:


### complete\_output
```python
  complete_output()
```

It disconnects ``self.outputBuffer`` from ``stdout`` and replaces with ``sys.stdout = sys.__stdout__``,
``sys.stderr = sys.__stderr__``
writes buffer data to log file ``if self.log_file is True``

**Returns**:

  It returns buffer ``output``

### stopTest
```python
  stopTest(test)
```

Calls ``addSuccess()`` if testcase passed.
Calls ``addError()`` if gets error while testing.
Calls ``addFailure()`` if test has failed.
It disconnects ``self.outputBuffer`` from ``stdout`` and replaces with ``sys.__stdout__``

**Arguments**:

- `test` - Testcase to stop after it runs
  

**Returns**:


### addSuccess
```python
  addSuccess(test)
```

It override method of ``class unittest.TestResult``
It writes P in console

**Arguments**:

- `test` - Testcase
  

**Returns**:


### addError
```python
  addError(test, err)
```

It override method of ``class unittest.TestResult``
It writes E in console

**Arguments**:

- `test` - Testcase
  

**Returns**:

### addFailure
```python
  addFailure(test, err)
```

It override method of ``class unittest.TestResult``
It writes F in console

**Arguments**:

- `test` - TestCase
  

**Returns**:



## HTMLTestRunner Objects
```python
class HTMLTestRunner()
```


### \_\_init\_\_
```python
  __init__(log=None, output=None, verbosity=1, title=None, description=None, report_name='report', open_in_browser=False)
```

HTMLTestRunner

**Arguments**:

- `self` _HTMLTestRunner_ - Object of HTMLTestRunner
- `log` _bool_ - If ``True`` it logs print buffer to *.txt file with timestamp
- `output` _str_ - Report output dir name
- `verbosity` _int_ - If ``verbosity > 1`` it prints brief summary of testcases in console
- `title` _str_ - Title of the Test Report
- `description` _str_ - Description of Test Report
- `report_name` _str_ - Starting name of Test report and log file
- `open_in_browser` _bool_ - If ``True`` it opens report in browser automatically
  

**Returns**:

  Runner object


### run
```python
  run(test)
```

Run the Test Case

**Arguments**:

- `test` - Test Case
  

**Returns**:

  It returns ``result``

### sortResult
```python
  sortResult(result_list)
```

It sorts the Testcases to run

**Arguments**:

- `result_list` _list_ - Results list
  

**Returns**:

  Returns sorted result list

### getReportAttributes
```python
  getReportAttributes(result)
```

Return report attributes as a list of (name, value).
Override this to add custom attributes.

### generateReport
```python
  generateReport(result)
```

It geneartes HTML report by using unittest report
@param result:unittest result
After generates html report it opens report in browser if open_in_broser is True
It adds stylesheet and script files in reports directory

