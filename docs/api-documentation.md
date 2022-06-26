<!-- markdownlint-disable -->

<a href="../HTMLTestRunner/runner.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `runner.py`
HTMLTestRunner-rv module to generate HTML report for your testcase ================================================================== 

The HTMLTestRunner provides easy way to generate HTML Test Reports. Easy to find errors and reduce the debug time. You no need to see console to see the debug messages, it logs every print logs in to *.txt with timestamp. So it is easy to debug whenever you want. 

*   It automatically opens report in your browser so no need to search report file in your directory.  Just you need to pass `open_in_browser = True`. 

*   Color of Testcase block automatically change as per test result. 

*   You can add your custom style Eg: style = "CSS styling" 

*   You can add your custom script Eg: script = "javascript"  



**Global Variables**
---------------
- **stdout_redirector**
- **stderr_redirector**
- **STATUS**
- **DEFAULT_TITLE**
- **DEFAULT_DESCRIPTION**
- **PKG_PATH**

---

<a href="../HTMLTestRunner/runner.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `to_string`

```python
to_string(s)
```

It converts strings to unicode 

**Args:**
 
 - <b>`s`</b> (str,byte):  String to convert to unicode 



**Returns:**
 It returns unicode 


---

## <kbd>class</kbd> `HTMLTestRunner`




<a href="../HTMLTestRunner/runner.py#L290"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    log=None,
    output=None,
    verbosity=1,
    title=None,
    description=None,
    style='',
    script='',
    report_name='report',
    open_in_browser=False,
    tested_by='Unknown',
    add_traceback=False
)
```

HTMLTestRunner 

**Args:**
 
 - <b>`self`</b> (HTMLTestRunner):  Object of HTMLTestRunner 
 - <b>`log`</b> (bool):  If ``True`` it logs print buffer to *.txt file with timestamp 
 - <b>`output`</b> (str):  Report output dir name 
 - <b>`verbosity`</b> (int):  If ``verbosity > 1`` it prints brief summary of testcases in console 
 - <b>`title`</b> (str):  Title of the Test Report 
 - <b>`description`</b> (str):  Description of Test Report 
 - <b>`style`</b> (str):  Custom style for report 
 - <b>`script`</b> (str):  Custom script for report 
 - <b>`report_name`</b> (str):  Starting name of Test report and log file 
 - <b>`open_in_browser`</b> (bool):  If ``True`` it opens report in browser automatically 
 - <b>`add_traceback`</b> (bool): Adds error trace back to report if True 



**Returns:**
 Runner object 




---

<a href="../HTMLTestRunner/runner.py#L398"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `generate_report`

```python
generate_report(result)
```

It generates HTML report by using unittest report @param result:unittest result After generates html report it opens report in browser if open_in_browser is True It adds stylesheet and script files in reports directory 

---

<a href="../HTMLTestRunner/runner.py#L372"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_report_attributes`

```python
get_report_attributes(result)
```

Return report attributes as a list of (name, value). Override this to add custom attributes. 

---

<a href="../HTMLTestRunner/runner.py#L336"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `run`

```python
run(test)
```

Run the Test Case 

**Args:**
 
 - <b>`test`</b>:  Test Case 



**Returns:**
 It returns ``result`` 

---

<a href="../HTMLTestRunner/runner.py#L351"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `sort_result`

```python
sort_result(result_list)
```

It sorts the Testcases to run 

**Args:**
 
 - <b>`result_list`</b> (list):  Results list 



**Returns:**
 Returns sorted result list 


---

## <kbd>class</kbd> `OutputRedirector`
Wrapper to redirect stdout or stderr 

<a href="../HTMLTestRunner/runner.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(fp)
```

Wrapper to redirect stdout or stderr 

**Args:**
 
 - <b>`fp`</b> (buffer):  Buffer to store stdout 




---

<a href="../HTMLTestRunner/runner.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `flush`

```python
flush()
```

It flushes string buffer 

**Returns:**
 

---

<a href="../HTMLTestRunner/runner.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `write`

```python
write(s)
```

Write to string buffer with timestamp 

**Args:**
 
 - <b>`s`</b> (str):  String to write to buffer 



**Returns:**
  It returns None 

---

<a href="../HTMLTestRunner/runner.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `writelines`

```python
writelines(lines)
```

It writes number lines to buffer 

**Args:**
 
 - <b>`lines`</b> (list):  List of lines to write to buffer 



**Returns:**
 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
