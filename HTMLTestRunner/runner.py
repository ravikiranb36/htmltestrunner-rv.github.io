"""
# HTMLTestRunner

HTMLTestRunner for python unit test

A TestRunner for use with the Python unit testing framework. It generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g.
import unittest
from HTMLTestRunner import HTMLTestRunner
... define your tests ... For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

# Creating suite

my_test_suite = unittest.TestSuite()

# output to a file

runner = HTMLTestRunner(title='My unit test', open_in_browser=True)

# run the test

runner.run(my_test_suite)
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
__version__ = "1.0.11"

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import os
import re
from io import StringIO
import sys
import time
import unittest
import shutil
from jinja2 import Environment, FileSystemLoader
# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>
from pyparsing import unicode


def to_unicode(s):
    try:
        return unicode(s)
    except UnicodeDecodeError:
        # s is non ascii byte string
        return s.decode('unicode_escape')


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(to_unicode(s))

    def writelines(self, lines):
        lines = map(to_unicode, lines)
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

STATUS = {
    0: 'PASS',
    1: 'FAIL',
    2: 'ERROR',
}

DEFAULT_TITLE = 'Unit Test Report'
DEFAULT_DESCRIPTION = ''
pkg_path = os.path.dirname(__file__)
TestResult = unittest.TestResult


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.outputBuffer = StringIO()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        output = self.outputBuffer.getvalue()
        self.outputBuffer.truncate(0)
        return output

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
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
    """
    """

    def __init__(self, stream=None, output=None, verbosity=1, title=None, description=None, report_name='report',
                 open_in_browser=False):
        self.stream = stream
        self.report_name = report_name
        self.output = output
        self.open_in_browser = open_in_browser
        if self.output is None:
            self.output = './reports/'
        self.verbosity = verbosity
        if title is None:
            self.title = DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now()

    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
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
        ]

    def generateReport(self, result):

        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        report = self._generate_report(result)
        env = Environment(loader=FileSystemLoader(os.path.join(pkg_path,'templates')))
        template = env.get_template('template.html')
        output = template.render(
            generator=generator,
            report_attrs=report_attrs,
            title=self.title,
            report=report,
            stop_time=(self.stopTime - self.startTime),
        )
        if self.stream is not None:
            self.stream.write(output)
        html_report_file_name = f'{self.output}{self.report_name}_{time.strftime("%d-%m-%y %I-%M-%S")}.html'
        os.makedirs(os.path.dirname(html_report_file_name), exist_ok=True)
        shutil.copy(os.path.join(pkg_path,'static','stylesheet.css'), f'{self.output}stylesheet.css')
        shutil.copy(os.path.join(pkg_path,'static','script.js'), f'{self.output}script.js')
        with open(html_report_file_name, 'w') as file:
            file.write(output)
        if self.open_in_browser:
            import webbrowser
            webbrowser.open_new_tab('file:///' + os.getcwd() + html_report_file_name)

    def _generate_report(self, result):
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
            d_row = {
                'style': ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                'desc': desc,
                'count': np + nf + ne,
                'pass': np,
                'fail': nf,
                'error': ne,
                'cid': 'c%s' % (cid + 1),
                'fun_testcases': fun_testcases,
            }
            class_testcases.append(d_row)
        report = {
            'class_testcases': class_testcases,
            'count': str(result.success_count + result.failure_count + result.error_count),
            'pass': str(result.success_count),
            'fail': str(result.failure_count),
            'error': str(result.error_count),
        }
        return report

    def _generate_report_test(self, fun_testcases, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name

        # o and e should be byte string because they are collected from stdout and stderr?
        if not isinstance(o, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            uo = o.decode('latin-1')
        else:
            uo = o
        if not isinstance(e, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            ue = e.decode('latin-1')
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
        if not has_output:
            return


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
