"""
# HTMLTestRunner
```text
HTMLTestRunner for python unit test

A TestRunner for use with the Python unit testing framework.
It generates a HTML report to show the result at a glance.
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
    runner = HTMLTestRunner(log=True, verbosity=2, output='report', title='Test report', report_name='report',
                                open_in_browser=True, description="HTMLTestReport")
    runner.run(suite)
if __name__ == '__main__':
    test_suite()
```
------------------------------------------------------------------------
Copyright (c) 2020-2025, Ravikirana B
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Ravikirana B nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = "Ravikirana B"
__version__ = "1.0.12"

from datetime import datetime
import os
import re
from io import StringIO
import sys
import time
import unittest
import shutil
from jinja2 import Environment, FileSystemLoader

from pyparsing import unicode


def to_unicode(s):
    """
    To convert unicode
    """
    try:
        return unicode(s)
    except UnicodeDecodeError:
        # s is non ascii byte string
        return s.decode('utf-8', 'ignore')


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        """
        Write to string buffer with timestamp
        """
        string = to_unicode(s)
        if string == '\n' or string == ' ':
            pass
        else:
            output = str(datetime.now()) + ' : ' + string.replace('\n', '\n' + ' ' * 29) + '\n'
            self.fp.write(output)

    def writelines(self, lines):
        lines = map(to_unicode, lines)
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

# Test status
STATUS = {
    0: 'PASS',
    1: 'FAIL',
    2: 'ERROR',
}

DEFAULT_TITLE = 'Unit Test Report'
DEFAULT_DESCRIPTION = 'Test report generation using HTMLTestRunner-rv'

PKG_PATH = os.path.dirname(__file__)
TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1, log_file=''):
        TestResult.__init__(self)
        self.log_file = log_file
        self.outputBuffer = StringIO()
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.result = []

    def startTest(self, test):
        """
        Start test inherited by unittest TestResult
        """
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        writes buffer data to log file if self.log_file is True
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        output = self.outputBuffer.getvalue()
        self.outputBuffer.seek(0)
        self.outputBuffer.truncate(0)
        # Writing buffer data to log file
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(output)
        return output

    def stopTest(self, test):
        """
        Usually one of addSuccess, addError or addFailure would have been called.
        But there are some path in unittest that would bypass this.
        We must disconnect stdout in stopTest(), which is guaranteed to be called.
        """
        self.complete_output()

    def addSuccess(self, test):
        """
        It calls if the test passes and writes P in stdout
        """
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stdout.write('P')

    def addError(self, test, err):
        """
        It calls if the test fails and writes E in stderr
        """
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        """
        It calls if gets error and writes E in stderr
        """
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class HTMLTestRunner:
    """HTMLTestRunner class"""

    def __init__(self, log=None, output=None, verbosity=1, title=None, description=None, report_name='report',
                 open_in_browser=False):
        """
        @param log: bool If it is True start logs to txt file with timestamp
        @param verbosity: If it's more than 1 it logs with more details
        @param output: Report directory
        @param title:Report title
        @param description:Test report descriptin
        @param report_name:report name starts with
        @param open_in_browser:bool If it is True opens report automatically in browser
        """
        self.report_name = report_name
        self.output = output
        if self.output is None:
            self.output = 'reports'
        self.open_in_browser = open_in_browser
        self.html_report_file_name = f'./{self.output}/{self.report_name}_{time.strftime("%d-%m-%y %I-%M-%S")}.html'
        os.makedirs(os.path.dirname(self.html_report_file_name), exist_ok=True)
        self.log_file = ''
        if log:
            self.log_file = f'./{self.output}/{self.report_name}_{time.strftime("%d-%m-%y %I-%M-%S")}_log.txt'
        self.verbosity = verbosity
        if title is None:
            self.title = DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.now()

    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity, self.log_file)
        test(result)
        self.stopTime = datetime.now()
        self.generateReport(result)
        return result

    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.success_count: status.append('Pass %s' % result.success_count)
        if result.failure_count: status.append('Failure %s' % result.failure_count)
        if result.error_count:   status.append('Error %s' % result.error_count)
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            ('Start Time', startTime),
            ('Duration', duration),
            ('Status', status),
            ('Descrition', self.description)
        ]

    def generateReport(self, result):
        """
        It geneartes HTML report by using unittest report
        @param result:unittest result
        After generates html report it opens report in browser if open_in_broser is True
        It adds stylesheet and script files in reports directory
        """
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        report = self._generate_report(result)
        env = Environment(loader=FileSystemLoader(os.path.join(PKG_PATH, 'templates')))
        template = env.get_template('template.html')
        output = template.render(
            generator=generator,
            report_attrs=report_attrs,
            title=self.title,
            report=report,
            stop_time=(self.stopTime - self.startTime),
        )

        shutil.copy(os.path.join(PKG_PATH, 'static', 'stylesheet.css'), f'./{self.output}/stylesheet.css')
        shutil.copy(os.path.join(PKG_PATH, 'static', 'script.js'), f'./{self.output}/script.js')
        with open(self.html_report_file_name, 'w') as file:
            file.write(output)
        if self.open_in_browser:
            import webbrowser
            webbrowser.open_new_tab('file:///' + os.getcwd() + self.html_report_file_name)

    def _generate_report(self, result):
        '''It generates the report'''
        class_testcases = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            fun_testcases = []
            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(fun_testcases, cid, tid, n, t, o, e)
            cls_testcase = {
                'style': ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                'desc': desc,
                'count': np + nf + ne,
                'pass': np,
                'fail': nf,
                'error': ne,
                'cid': 'c%s' % (cid + 1),
                'fun_testcases': fun_testcases,
            }
            class_testcases.append(cls_testcase)
        report = {
            'class_testcases': class_testcases,
            'count': str(result.success_count + result.failure_count + result.error_count),
            'pass': str(result.success_count),
            'fail': str(result.failure_count),
            'error': str(result.error_count),
        }
        return report

    def _generate_report_test(self, fun_testcases, cid, tid, n, t, o, e):
        """
        It generates report for each testcase functions
        """
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        if not has_output:
            return
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name

        # o and e should be byte string because they are collected from stdout and stderr?
        if not isinstance(o, str):
            uo = o.decode('utf-8', 'ignore')
        else:
            uo = o
        if not isinstance(e, str):
            ue = e.decode('utf-8', 'ignore')
        else:
            ue = e

        log = uo
        error = ue
        testcase = {
            'tid': tid,
            'class': (n == 0 and 'hiddenRow' or 'none'),
            'style': n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
            'desc': desc,
            'log': re.sub('\x00', '', log),
            'error': error,
            'status': STATUS[n],
        }
        fun_testcases.append(testcase)
