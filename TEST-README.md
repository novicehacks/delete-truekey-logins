# Test Suite for TrueKey Login Deleter Script

This directory contains a comprehensive test suite for the TrueKey Login Deleter Script using pytest and unittest.mock.

## Test Structure

### Test Files

- **`test_delete_truekey_logins.py`** - Main test suite with unit and integration tests
- **`test_mocks.py`** - Reusable mock objects and utilities for testing
- **`run_tests.py`** - Test runner script with various options
- **`pytest.ini`** - Pytest configuration file
- **`requirements-test.txt`** - Test dependencies

### Test Categories

#### Unit Tests
- Chrome process detection and management
- TrueKey profile setup and management
- Chrome WebDriver configuration
- Extension ID validation and configuration
- Argument parsing
- Element detection and interaction

#### Integration Tests
- Complete workflow testing
- End-to-end deletion process
- Browser automation flow

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

### Basic Test Execution

```bash
# Run all tests
python run_tests.py

# Run with pytest directly
pytest test_delete_truekey_logins.py -v

# Run specific test categories
python run_tests.py --unit
python run_tests.py --integration
```

### Advanced Test Options

```bash
# Run tests with coverage report
python run_tests.py --coverage

# Run with verbose output
python run_tests.py --verbose

# Run tests with specific markers
python run_tests.py --markers unit mock

# Check dependencies
python run_tests.py --check-deps
```

### Pytest Options

```bash
# Run specific test methods
pytest test_delete_truekey_logins.py::TestTrueKeyDeletionScript::test_chrome_process_detection_running -v

# Run tests with specific markers
pytest -m unit -v
pytest -m integration -v

# Run with coverage
pytest --cov=. --cov-report=html -v

# Run tests in parallel (if pytest-xdist is installed)
pytest -n auto -v
```

## Test Coverage

The test suite covers:

- ✅ Chrome process management
- ✅ Profile setup and copying
- ✅ WebDriver creation and configuration
- ✅ Extension dashboard navigation
- ✅ List mode switching
- ✅ Trash icon detection
- ✅ Deletion process with confirmation dialogs
- ✅ Extension ID validation
- ✅ Argument parsing
- ✅ Complete workflow integration

## Mock Objects

### Chrome Profile Mock
- Simulates Chrome profile structure
- Creates mock preference files
- Handles profile copying operations

### WebDriver Mock
- Mocks Selenium WebDriver functionality
- Simulates element finding and interaction
- Tracks method calls for verification

### Subprocess Mock
- Mocks Chrome process detection
- Simulates process termination
- Handles system command execution

### WebElement Mock
- Mocks Selenium WebElement behavior
- Simulates clicking and interaction
- Tracks element state

## Test Data

### Extension IDs
- Valid extension IDs (32 characters, lowercase alphanumeric)
- Invalid extension IDs (various formats)
- Default TrueKey extension ID

### Chrome Arguments
- Complete list of Chrome options used in the script
- Security bypasses and performance optimizations
- User experience enhancements

## Continuous Integration

The test suite is designed to run in CI/CD environments:

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements-test.txt
    - name: Run tests
      run: python run_tests.py --coverage
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all test dependencies are installed
   - Check Python path configuration

2. **Mock Failures**
   - Verify mock objects are properly configured
   - Check mock call expectations

3. **Selenium Errors**
   - Tests use mocks, so actual Selenium installation not required
   - Ensure selenium package is installed for type checking

### Test Debugging

```bash
# Run tests with debugging output
pytest -s -v test_delete_truekey_logins.py

# Run specific test with debugging
pytest -s -v test_delete_truekey_logins.py::TestTrueKeyDeletionScript::test_chrome_driver_creation

# Show test coverage details
pytest --cov=. --cov-report=term-missing -v
```

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Use descriptive test names
3. Add appropriate docstrings
4. Use the mock utilities from `test_mocks.py`
5. Update this README if adding new test categories

### Test Naming Convention

- Test classes: `TestFeatureName`
- Test methods: `test_specific_functionality`
- Mock objects: `MockObjectName`

### Adding New Mocks

1. Add mock class to `test_mocks.py`
2. Include cleanup methods where needed
3. Document mock behavior and usage
4. Add to test utilities if reusable

## Performance

The test suite is optimized for speed:
- Uses mocks to avoid browser automation
- Minimal file system operations
- Fast test execution (typically < 10 seconds)
- Parallel test execution support

## Security

Tests use mocks and temporary files:
- No actual browser automation
- No network requests
- Isolated test environment
- Automatic cleanup of test artifacts
