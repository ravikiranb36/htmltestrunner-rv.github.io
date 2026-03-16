# HTMLTestRunner-rv

[![PyPI version](https://badge.fury.io/py/HTMLTestRunner-rv.svg)](https://badge.fury.io/py/HTMLTestRunner-rv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.7+-blue.svg)](https://pypi.org/project/HTMLTestRunner-rv/)

**HTMLTestRunner-rv** is a professional, feature-rich HTML test report generator for the Python `unittest` framework. It provides a modern dashboard-style interface with detailed metrics, per-test timing, and interactive filtering to make debugging seamless.

[**Check the Live Documentation**](https://ravikiranb36.github.io/htmltestrunner-rv.github.io/)

---

## 🌟 Key Features

- **📊 Modern Dashboard:** A card-based overview of Pass, Fail, Error, and Skip rates.
- **🕒 Per-Test Duration:** Tracks the exact execution time for *every* test case.
- **🔍 Interactive Filtering:** Toggle views for Summary, Failed, Passed, or Errored tests with one click.
- **🖥️ Dark Terminal Theme:** Execution logs (stdout/stderr) are displayed in a professional dark terminal window.
- **🚀 Instant Feedback:** Optionally opens the generated report in your default browser automatically.
- **📁 Smart Logging:** Captures all print statements and errors into timestamped `.txt` files.
- **✅ Full unittest Support:** Supports `subTest`, `skip`, and all standard `unittest` features.

---

## 🛠️ Installation

Install the latest version of `HTMLTestRunner-rv` using pip:

```bash
pip install HTMLTestRunner-rv
```

---

## 🚀 Quick Start

Creating a professional test report is as simple as replacing your standard `unittest.TextTestRunner` with `HTMLTestRunner`.

### Simple Example

```python
import unittest
from HTMLTestRunner.runner import HTMLTestRunner

class MyTests(unittest.TestCase):
    def test_success(self):
        """A simple successful test"""
        print("Executing success test...")
        self.assertEqual(1, 1)

    def test_error(self):
        """A test that raises an error"""
        print("Executing error test...")
        return 1 / 0

if __name__ == '__main__':
    # Load your tests
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTests)
    
    # Initialize the runner
    runner = HTMLTestRunner(
        title='Test Report Review',
        description='Daily regression test results',
        tested_by='Your Name',
        open_in_browser=True
    )
    
    # Run the tests
    runner.run(suite)
```

---

## ⚙️ Configuration Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `output` | `str` | `'reports'` | Directory where the HTML report and logs will be saved. |
| `report_name` | `str` | `'report'` | The prefix for the generated report file name. |
| `title` | `str` | `'Test Report Review'` | The title displayed at the top of the HTML report. |
| `description` | `str` | `None` | A brief description of the test suite. |
| `verbosity` | `int` | `1` | Controls the console output detail level. |
| `log` | `bool` | `False` | If `True`, captures all print statements to a timestamped `.txt` file. |
| `open_in_browser` | `bool` | `False` | Automatically opens the report in your web browser after completion. |
| `add_traceback` | `bool` | `True` | Includes full error tracebacks in the report. |
| `tested_by` | `str` | `'Unknown'` | Name of the person or system that ran the tests. |
| `style` | `str` | `""` | Custom CSS string to inject into the report. |
| `script` | `str` | `""` | Custom JavaScript string to inject into the report. |

---

## 📝 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

---

## 🤝 Sponsorship & Funding

This project is proudly funded and supported by **[RV Anveshana](https://rvanveshana.com/)**. Their commitment to open-source innovation helps maintain and evolve this framework for the developer community.

---

## 💰 Support the Project

If you find this tool useful, please consider supporting its development. Your contribution helps us maintain and improve this framework.

**[👉 Click here for donation](https://razorpay.me/@ravikiranabyadarahalli)**

---

**Developed by Ravikirana B** - [ravikiranb36@gmail.com](mailto:ravikiranb36@gmail.com)
