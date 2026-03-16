# About HTMLTestRunner-rv

**HTMLTestRunner-rv** is an enhanced, feature-rich version of the original `HTMLTestRunner` for Python's `unittest` framework. This project focuses on delivering professional-grade, interactive HTML reports that are aesthetically pleasing and highly informative.

## Why HTMLTestRunner-rv?

While the original runner was groundbreaking, modern software development requires more detailed insights and better visualizations. This version addresses several key areas:

### 1. Modern Presentation
We've replaced outdated tables with a sleek, card-based dashboard that highlights the most critical metrics immediately. The report uses a professional color palette to distinguish between different test statuses at a glance.

### 2. Time-Aware Reporting
Unlike older versions, **HTMLTestRunner-rv** tracks:
- **Start Time** of the entire suite.
- **End Time** of the entire suite.
- **Duration** for *every single* test case, helping you identify performance bottlenecks quickly.

### 3. Smart Filtering
The report includes built-in interactive filters that allow you to:
- See a high-level **Summary**.
- Quickly isolate **Failed** or **Errored** tests.
- View **Skipped** tests to ensure coverage.
- Toggle visibility for an entire class of tests with a single click.

### 4. Robust Execution Logs
Execution logs (stdout/stderr) are presented in a dark-themed terminal window, making them easier to read. The runner also ensures proper handling of `bytes` decoding and removes any problematic characters that could break the report.

## Technology Stack
- **Backend:** Python 3.7+ (supports up to Python 3.13)
- **Templating:** Jinja2 for clean separation of logic and presentation.
- **Frontend:** Modern CSS Grid/Flexbox and lightweight Vanilla JavaScript.

## Compatibility
Fully compatible with all standard `unittest` features, including:
- `unittest.skip`, `unittest.skipIf`, `unittest.skipUnless`
- `subTest` (Sub-test results are grouped naturally under their parent test)
- All custom `TestCase` classes.
