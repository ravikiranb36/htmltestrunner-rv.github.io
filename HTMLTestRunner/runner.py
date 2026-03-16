# -*- coding: utf-8 -*-
# module runner.py
#
# Copyright (c) 2021-2030  Ravikirana B
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
"""
HTMLTestRunner-rv core module.
==============================

This module provides the main `HTMLTestRunner` class, which extends `unittest.TextTestRunner`
capabilities to generate professional-grade HTML reports. It includes built-in support for
capturing output, tracking execution timing, and a dashboard-style visualization.
"""

__author__ = "Ravikirana B ravikiranb36@gmail.com"
__all__ = ['HTMLTestRunner']
__version__ = '1.1.3'

import os
import re
import shutil
import sys
import time
import unittest
from datetime import datetime
from io import StringIO

from jinja2 import Environment, FileSystemLoader


def convert_to_string(input_data):
    """
    Safely converts input data (string or bytes) into a Unicode string.

    Args:
        input_data (str|bytes): The data to be converted.

    Returns:
        str: The decoded Unicode string.

    Raises:
        Exception: If the input data is not string or bytes.
    """
    try:
        if isinstance(input_data, str):
            return input_data
        elif isinstance(input_data, bytes):
            return input_data.decode("utf-8", "ignore")
        else:
            raise Exception(f"{input_data} is not string or bytes")
    except Exception as e:
        return str(e)


class OutputRedirector:
    """
    Intercepts and redirects stdout or stderr to a string buffer.
    
    This class prepends a timestamp to every line written to the buffer
    to provide a clear execution timeline within the final report.
    """

    def __init__(self, file_pointer):
        """
        Initializes the redirector with a target buffer.

        Args:
            file_pointer (StringIO): The buffer where output will be stored.
        """
        self.file_pointer = file_pointer

    def write(self, text):
        """
        Writes text to the buffer, adding timestamps to non-empty lines.

        Args:
            text (str): The text content to write.
        """
        content = convert_to_string(text)
        if content == '\n' or content == ' ':
            pass
        else:
            timestamped_output = str(datetime.now()) + ' : ' + content.replace('\n', '\n' + ' ' * 29) + '\n'
            self.file_pointer.write(timestamped_output)

    def writelines(self, lines):
        """
        Writes a list of lines to the buffer.

        Args:
            lines (list[str]): A list of strings to write.
        """
        lines = map(convert_to_string, lines)
        self.file_pointer.writelines(lines)

    def flush(self):
        """Flushes the underlying buffer."""
        self.file_pointer.flush()


# stdout redirected
stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

# Test status
TEST_STATUS_MAP = {
    0: 'PASS',
    1: 'FAIL',
    2: 'ERROR',
    3: 'SKIP',
}

DEFAULT_TITLE = 'Test Report Review'
DEFAULT_DESCRIPTION = 'Test report generation using HTMLTestRunner-rv'

PACKAGE_PATH = os.path.dirname(__file__)


class _TestResult(unittest.TestResult):
    """
    Internal results collector for HTMLTestRunner.
    
    This class captures metrics, output logs, and per-test duration for the report.
    """

    def __init__(self, verbosity=1, log_file='', add_traceback=False):
        super().__init__()
        self.log_file = log_file
        self.outputBuffer = StringIO()
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity
        self.results_list = []
        self.add_traceback = add_traceback
        self.test_start_time = None

    def startTest(self, test):
        super().startTest(test)
        self.test_start_time = time.time()
        # just one buffer for both stdout and stderr
        stdout_redirector.file_pointer = self.outputBuffer
        stderr_redirector.file_pointer = self.outputBuffer
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        output_content = self.outputBuffer.getvalue()
        self.outputBuffer.seek(0)
        self.outputBuffer.truncate(0)
        # Writing buffer data to log file
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(output_content)
        return output_content

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        duration = time.time() - self.test_start_time
        self.results_list.append((0, test, output, '', duration))
        if self.verbosity > 1:
            sys.stdout.write('ok ')
            sys.stdout.write(str(test))
            sys.stdout.write('\n')
        else:
            sys.stdout.write('P')

    def addError(self, test, err):
        self.error_count += 1
        super().addError(test, err)
        _, traceback_text = self.errors[-1]
        if not self.add_traceback:
            traceback_text = ''
        output = self.complete_output()
        duration = time.time() - self.test_start_time
        self.results_list.append((2, test, output, traceback_text, duration))
        if self.verbosity > 1:
            sys.stderr.write('E')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        super().addFailure(test, err)
        _, traceback_text = self.failures[-1]
        if not self.add_traceback:
            traceback_text = ''
        output = self.complete_output()
        duration = time.time() - self.test_start_time
        self.results_list.append((1, test, output, traceback_text, duration))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')

    def addSubTest(self, test: unittest.case.TestCase, subtest: unittest.case.TestCase, err) -> None:
        if err:
            self.failure_count += 1
            self.addFailure(subtest, err)
        else:
            self.addSuccess(subtest)

    def addSkip(self, test, reason):
        self.skip_count += 1
        super().addSkip(test, reason)
        output = self.complete_output()
        duration = time.time() - self.test_start_time
        self.results_list.append((3, test, output, reason, duration))
        if self.verbosity > 1:
            sys.stdout.write('skip ')
            sys.stdout.write(str(test))
            sys.stdout.write('\n')
        else:
            sys.stdout.write('S')


class HTMLTestRunner:
    """
    The main class for running unit tests and generating an HTML report.
    """

    def __init__(self, log=None, output=None, verbosity=1, title=None, description=None, style="", script="",
                 report_name='report', open_in_browser=False, tested_by="Unknown", add_traceback=True):
        """
        Initializes the HTMLTestRunner.

        Args:
            log (bool): If True, redirects print output to a timestamped log file.
            output (str): Directory name where the report and logs will be saved. Defaults to 'reports'.
            verbosity (int): Level of console output (0, 1, or 2).
            title (str): The title displayed at the top of the HTML report.
            description (str): A brief description displayed in the report metadata.
            style (str): Custom CSS string to inject into the report.
            script (str): Custom JavaScript string to inject into the report.
            report_name (str): The prefix for the generated report filename.
            open_in_browser (bool): Automatically open the generated report in the default web browser.
            tested_by (str): Name of the tester or system for the report footer.
            add_traceback (bool): Whether to include full Python tracebacks in the report.
        """
        self.stop_time = None
        self.add_traceback = add_traceback
        self.report_name = report_name
        self.style = style
        self.script = script
        self.tested_by = tested_by
        if output is None:
            output = 'reports'
        self.open_in_browser = open_in_browser
        self.output_dir = os.path.abspath(output)
        os.makedirs(self.output_dir, exist_ok=True)
        self.html_report_file_name = os.path.join(self.output_dir,
                                                  f'{self.report_name}_{time.strftime("%d-%m-%y %I-%M-%S")}.html')
        self.log_file = ''
        if log:
            self.log_file = os.path.join(self.output_dir,
                                         f'{self.report_name}_{time.strftime("%d-%m-%y %I-%M-%S")}_log.txt')
        self.verbosity = verbosity
        if title is None:
            self.title = DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.start_time = datetime.now()

    def run(self, test):
        """
        Runs the provided test suite or case.

        Args:
            test (unittest.TestSuite|unittest.TestCase): The test suite or case to execute.

        Returns:
            _TestResult: An object containing the captured test results.
        """
        result = _TestResult(self.verbosity, self.log_file, self.add_traceback)
        test(result)
        self.stop_time = datetime.now()
        self.generate_report(result)
        return result

    @staticmethod
    def sort_result(results_list):
        """
        Groups test results by their parent class for structured reporting.

        Args:
            results_list (list): The list of results from the TestResult object.

        Returns:
            list[tuple]: A list of tuples containing (test_class, results).
        """
        result_map = {}
        ordered_classes = []
        for status_code, test_case, output, error_message, duration in results_list:
            test_class = test_case.__class__
            if str(test_class) == "<class 'unittest.case._SubTest'>":
                test_class = ordered_classes[-1]
            if not test_class in result_map:
                result_map[test_class] = []
                ordered_classes.append(test_class)
            result_map[test_class].append((status_code, test_case, output, error_message, duration))
        
        sorted_results = [(test_class, result_map[test_class]) for test_class in ordered_classes]
        return sorted_results

    def get_report_attributes(self, result):
        """
        Collects summary attributes for the report header.

        Args:
            result (_TestResult): The captured test results.

        Returns:
            list[tuple]: Key-value pairs of report metadata.
        """
        start_time_str = str(self.start_time)[:19]
        stop_time_str = str(self.stop_time)[:19]
        elapsed_duration = str(self.stop_time - self.start_time)
        
        total_tests = result.success_count + result.failure_count + result.error_count + result.skip_count
        pass_rate = "0.00%"
        if total_tests > 0:
            pass_rate = f"{(result.success_count / total_tests) * 100:.2f}%"

        status_metrics = {
            'pass': result.success_count,
            'fail': result.failure_count,
            'error': result.error_count,
            'skip': result.skip_count,
            'total': total_tests
        }
            
        return [
            ('Start Time', start_time_str),
            ('End Time', stop_time_str),
            ('Duration', elapsed_duration),
            ('Status', status_metrics),
            ('Pass Rate', pass_rate),
            ('Description', self.description),
            ('Tested By', self.tested_by)
        ]

    def generate_report(self, result):
        """
        Generates the final HTML report and copies static assets.

        Args:
            result (_TestResult): The captured test results.
        """
        report_attributes = self.get_report_attributes(result)
        generator_name = 'HTMLTestRunner %s' % __version__
        report_data = self._generate_report_data(result)
        
        jinja_env = Environment(loader=FileSystemLoader(os.path.join(PACKAGE_PATH, 'templates')))
        report_template = jinja_env.get_template('template.html')
        
        rendered_html = report_template.render(
            generator=generator_name,
            report_attrs=report_attributes,
            title=self.title,
            report=report_data,
            style=self.style,
            script=self.script,
            stop_time=(self.stop_time - self.start_time),
        )

        shutil.copy(os.path.join(PACKAGE_PATH, 'static', 'stylesheet.css'), os.path.join(self.output_dir, 'stylesheet.css'))
        shutil.copy(os.path.join(PACKAGE_PATH, 'static', 'script.js'), os.path.join(self.output_dir, 'script.js'))
        
        with open(self.html_report_file_name, 'w') as file_handler:
            file_handler.write(rendered_html)
            
        if self.open_in_browser:
            import webbrowser
            absolute_report_path = os.path.abspath(self.html_report_file_name)
            webbrowser.open_new_tab(f'file:///{absolute_report_path}')

    def _generate_report_data(self, result):
        """Internal method to structure data for the Jinja2 template."""
        report_class_list = []
        sorted_results = self.sort_result(result.results_list)
        
        for class_index, (test_class, class_results) in enumerate(sorted_results):
            pass_count = fail_count = error_count = skip_count = 0
            for status_code, test_case, output, error_message, duration in class_results:
                if status_code == 0:
                    pass_count += 1
                elif status_code == 1:
                    fail_count += 1
                elif status_code == 2:
                    error_count += 1
                else:
                    skip_count += 1

            if test_class.__module__ == "__main__":
                class_name = test_class.__name__
            else:
                class_name = "%s.%s" % (test_class.__module__, test_class.__name__)
            
            doc_string = test_class.__doc__ and test_class.__doc__.split("\n")[0] or ""
            class_description = doc_string and '%s: %s' % (class_name, doc_string) or class_name

            test_case_results = []
            for test_index, (status_code, test_case, output, error_message, duration) in enumerate(class_results):
                self._format_test_case_result(test_case_results, class_index, test_index, status_code, test_case, output, error_message, duration)
            
            class_data = {
                'style': error_count > 0 and 'errorClass' or fail_count > 0 and 'failClass' or 'passClass',
                'desc': class_description,
                'count': pass_count + fail_count + error_count + skip_count,
                'pass': pass_count,
                'fail': fail_count,
                'error': error_count,
                'skip': skip_count,
                'cid': f'c{class_index + 1}',
                'fun_testcases': test_case_results,
            }
            report_class_list.append(class_data)
            
        report_summary = {
            'class_testcases': report_class_list,
            'count': str(result.success_count + result.failure_count + result.error_count + result.skip_count),
            'pass': str(result.success_count),
            'fail': str(result.failure_count),
            'error': str(result.error_count),
            'skip': str(result.skip_count),
        }
        return report_summary

    @staticmethod
    def _format_test_case_result(test_case_results, class_index, test_index, status_code, test_case, output, error_message, duration):
        """Internal method to format individual test case data."""
        if status_code == 0:
            id_prefix = 'p'
        elif status_code == 1:
            id_prefix = 'f'
        elif status_code == 2:
            id_prefix = 'e'
        elif status_code == 3:
            id_prefix = 's'
        else:
            id_prefix = 'u' # unknown
            
        test_id = id_prefix + f't{class_index + 1}.{test_index + 1}'
        method_name = test_case.id().split('.')[-1]
        doc_string = test_case.shortDescription() or ""
        test_description = doc_string and ('%s: %s' % (method_name, doc_string)) or method_name

        clean_log = re.sub('\x00', '', convert_to_string(output))
        clean_error = convert_to_string(error_message)
        
        test_case_data = {
            'tid': test_id,
            'class': (status_code == 0 and 'hiddenRow' or 'none'),
            'style': status_code == 2 and 'errorCase' or (status_code == 1 and 'failCase' or (status_code == 3 and 'skipCase' or 'passCase')),
            'desc': test_description,
            'log': clean_log,
            'error': clean_error,
            'status': TEST_STATUS_MAP[status_code],
            'duration': f'{duration:.3f}s',
        }
        test_case_results.append(test_case_data)
