# HTMLTestRunner-rv

**HTMLTestRunner-rv** is a modernized version of the popular HTMLTestRunner, designed for Python 3.7+ with a focus on professional aesthetics, detailed metrics, and ease of use.

```text
Professional HTML Reporting for Python unittest
- Visual Dashboard with key metrics
- Per-test execution timing
- Built-in filtering (Summary, Pass, Fail, Error, Skip)
- Comprehensive execution logs with dark terminal theme
- Full support for subtests and skipped tests
```

[**Click here for Full Documentation**](https://ravikiranb36.github.io/htmltestrunner-rv.github.io/)

## Installation

```bash
pip install HTMLTestRunner-rv
```

## Quick Start

### 1. Create your Test Suite
```python
import unittest
from HTMLTestRunner.runner import HTMLTestRunner

# Import your test cases
from tests.my_test_file import MyTestCase

def create_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(MyTestCase))
    return suite
```

### 2. Run with HTMLTestRunner
```python
if __name__ == '__main__':
    runner = HTMLTestRunner(
        title='Test Report Review',
        description='Initial verification of the system',
        tested_by='Your Name',
        open_in_browser=True
    )
    runner.run(create_suite())
```

## Key Features

- **Aesthetic Dashboard:** At-a-glance summary of Pass/Fail/Error/Skip rates.
- **Timing:** Every test case includes its precise execution duration.
- **Filtering:** Interactive filters to isolate failed or errored tests quickly.
- **Clean API:** Refactored for readability and modern Python standards.
- **Metadata:** Tracks start time, end time, and total duration automatically.

## Support the Project
If you find this project useful, consider supporting it:
- [Click here for Donation](https://razorpay.me/@ravikiranabyadarahalli)
