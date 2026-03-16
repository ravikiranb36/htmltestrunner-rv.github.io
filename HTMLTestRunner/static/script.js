/**
 * Filters the test results displayed in the table based on their status.
 * @param {string} statusToDisplay - The status to filter by ('all', 'pass', 'fail', 'error', 'skip').
 */
function filterTests(statusToDisplay) {
    const testCaseRows = document.querySelectorAll('.test-case-row');
    const testClassRows = document.querySelectorAll('.test-class-row');
    const filterButtons = document.querySelectorAll('.btn-filter');

    // Update active state of filter buttons
    filterButtons.forEach(button => {
        if (button.id === `filter-${statusToDisplay}`) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });

    // Step 1: Filter individual test case rows
    testCaseRows.forEach(row => {
        const rowStatus = row.getAttribute('data-status');
        const logWindow = document.getElementById(`log-container-${row.id}`);

        if (statusToDisplay === 'all') {
            // In 'Summary' mode, we hide all individual test cases by default
            row.classList.add('hiddenRow');
            if (logWindow) logWindow.style.display = 'none';
        } else if (statusToDisplay === rowStatus) {
            // Show only matching test cases
            row.classList.remove('hiddenRow');
        } else {
            // Hide non-matching test cases
            row.classList.add('hiddenRow');
            if (logWindow) logWindow.style.display = 'none';
        }
    });

    // Step 2: Auto-hide/show test class group headers based on visible children
    testClassRows.forEach(classRow => {
        const classId = classRow.getAttribute('data-class-id');
        
        if (statusToDisplay === 'all') {
            // Always show class headers in summary mode
            classRow.style.display = '';
        } else {
            // In specific filter mode, hide class header if it has no visible tests
            const hasVisibleTests = document.querySelector(`.test-case-row[data-parent-class="${classId}"][data-status="${statusToDisplay}"]`);
            classRow.style.display = hasVisibleTests ? '' : 'none';
        }
    });
}

/**
 * Toggles the visibility of all test cases belonging to a specific class.
 * @param {string} classId - The ID of the test class to toggle.
 */
function toggleTestClassGroup(classId) {
    const siblingTestCases = document.querySelectorAll(`.test-case-row[data-parent-class="${classId}"]`);
    let targetDisplayIsHidden = true;

    // Determine if we should show or hide based on the first sibling's current state
    if (siblingTestCases.length > 0) {
        targetDisplayIsHidden = !siblingTestCases[0].classList.contains('hiddenRow');
    }

    siblingTestCases.forEach(row => {
        if (targetDisplayIsHidden) {
            row.classList.add('hiddenRow');
            // Also close any open logs when hiding the row
            const logWindow = document.getElementById(`log-container-${row.id}`);
            if (logWindow) logWindow.style.display = 'none';
        } else {
            row.classList.remove('hiddenRow');
        }
    });
}

/**
 * Toggles the visibility of a specific test execution log window.
 * @param {string} logContainerId - The HTML ID of the log container element.
 */
function toggleTestLog(logContainerId) {
    const logElement = document.getElementById(logContainerId);
    if (logElement) {
        const isCurrentlyVisible = logElement.style.display === 'block';
        logElement.style.display = isCurrentlyVisible ? 'none' : 'block';
    }
}

// Ensure the UI is correctly initialized when the page loads
window.addEventListener('DOMContentLoaded', () => {
    // We start in 'Summary' mode (filter='all')
    filterTests('all');
});
