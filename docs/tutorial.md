# Getting Started with HTMLTestRunner-rv

Follow this step-by-step guide to integrate **HTMLTestRunner-rv** into your projects.

## 1. Installation

Install the package via `pip`:

```bash
pip install HTMLTestRunner-rv
```

## 2. Basic Setup

First, import the necessary modules:

```python
import unittest
from HTMLTestRunner.runner import HTMLTestRunner

# Import your test cases from your project files
from tests.test_authentication import TestAuth
from tests.test_database import TestDB
```

## 3. Creating a Test Suite

The most effective way to manage multiple test cases is to create a suite:

```python
def create_test_suite():
    # Use TestLoader for modern compatibility (Python 3.7+)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Load all tests from specific classes
    suite.addTest(loader.loadTestsFromTestCase(TestAuth))
    suite.addTest(loader.loadTestsFromTestCase(TestDB))
    
    return suite
```

## 4. Running and Generating the Report

Initialize the `HTMLTestRunner` with your desired configuration:

```python
if __name__ == '__main__':
    # Define the runner with custom attributes
    runner = HTMLTestRunner(
        output='reports',             # Directory where the report will be saved
        title='Test Report Review',   # Title shown at the top of the report
        description='Daily regression test results',
        tested_by='Quality Assurance Team',
        open_in_browser=True,         # Automatically opens the report after execution
        log=True                      # Save console output to a separate log file
    )
    
    # Run the suite
    runner.run(create_test_suite())
```

## Advanced Features

### Handling Errors and Tracebacks
By default, the runner includes full error tracebacks. If you need to disable them for a cleaner report, set `add_traceback=False`:

```python
runner = HTMLTestRunner(add_traceback=False)
```

## Custom Styling & CSS Mapping

You can inject your own CSS to completely override the report's appearance using the `style` parameter.

### Core CSS Classes
To effectively customize the report, you can target these specific classes:

| Element | CSS Class | Description |
| :--- | :--- | :--- |
| **Main Title** | `h1` | The large title at the very top. |
| **Header Card** | `.report-header` | The white container holding metadata. |
| **Dashboard Card** | `.summary-card` | The individual metric cards (Total, Pass, etc.). |
| **Test Class Row** | `.test-class-row` | The row representing a Python test class. |
| **Test Case Row** | `.test-case-row` | The row representing an individual test method. |
| **Status Button** | `.status-btn` | The color-coded status button (PASS, FAIL, etc.). |
| **Log Window** | `.log-window` | The terminal-style log container. |

### Status-Specific Styling
The runner applies specific classes based on the test result:

- **Pass:** `.passClass` (row) and `.btn-pass` (button)
- **Fail:** `.failClass` (row) and `.btn-fail` (button)
- **Error:** `.errorClass` (row) and `.btn-error` (button)
- **Skip:** `.skipClass` (row) and `.btn-skip` (button)

### Example: Dark Theme Override
```python
dark_theme_css = """
    body { background-color: #121212; color: #e0e0e0; }
    .report-header, .summary-card, .test-report-table { 
        background: #1e1e1e; 
        color: #ffffff; 
        border: 1px solid #333; 
    }
    .test-class-row { background: #252525; }
    .table-header-row { background: #333333; }
"""

runner = HTMLTestRunner(style=dark_theme_css)
```

## Pro Tips
- **Filter Early:** Use the buttons at the top of the generated report to focus on failed tests first.
- **Check Durations:** Use the per-test timing column to find slow-running tests.
- **Support the Project:** This project is proudly funded by **[RV Anveshana](https://rvanveshana.com/)**. Consider donating to support further development!
