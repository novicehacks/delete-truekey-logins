# GitHub Actions Workflows

This repository uses GitHub Actions for continuous integration and deployment. The workflows are designed to provide fast feedback on commits and comprehensive testing on pull requests.

## Workflow Overview

### 🔄 Unit Tests (`unit-tests.yml`)
- **Trigger**: Every push to any branch
- **Purpose**: Fast feedback on basic functionality
- **Duration**: ~2-3 minutes
- **Python Versions**: 3.9, 3.11, 3.12
- **Tests**: Basic unit tests using `simple_test_runner.py`

### 🧪 Full Test Suite (`full-tests.yml`)
- **Trigger**: Pull requests to main branch, pushes to main
- **Purpose**: Comprehensive testing and quality assurance
- **Duration**: ~5-10 minutes
- **Python Versions**: 3.9, 3.11, 3.12
- **Operating Systems**: Ubuntu, Windows, macOS
- **Tests**: Full pytest suite with coverage, code quality checks

## Workflow Features

### ✅ Testing Strategy
- **Unit Tests**: Fast, basic functionality tests on every commit
- **Integration Tests**: Comprehensive testing on PR merges
- **Cross-Platform**: Tests on Ubuntu, Windows, and macOS
- **Multi-Version**: Tests on multiple Python versions

### 📊 Coverage Reporting
- Code coverage reports generated with pytest-cov
- HTML coverage reports uploaded as artifacts
- Codecov integration for coverage tracking
- Coverage reports available for 30 days

### 🔍 Code Quality
- **Black**: Code formatting checks
- **isort**: Import sorting validation
- **flake8**: Code style and error detection
- **bandit**: Security vulnerability scanning
- **safety**: Known vulnerability checks

### 📦 Build & Package
- Package building with `python -m build`
- Distribution artifacts uploaded
- Twine compatibility verification

## Status Badges

Add these badges to your README.md:

```markdown
[![Unit Tests](https://github.com/novicehacks/delete-truekey-logins/workflows/Unit%20Tests/badge.svg)](https://github.com/novicehacks/delete-truekey-logins/actions/workflows/unit-tests.yml)
[![Full Test Suite](https://github.com/novicehacks/delete-truekey-logins/workflows/Full%20Test%20Suite/badge.svg)](https://github.com/novicehacks/delete-truekey-logins/actions/workflows/full-tests.yml)
[![Code Coverage](https://codecov.io/gh/novicehacks/delete-truekey-logins/branch/main/graph/badge.svg)](https://codecov.io/gh/novicehacks/delete-truekey-logins)
```

## Local Development

### Quick Setup
```bash
# Run the development setup script
./setup-dev.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-test.txt

# Run basic tests
python3 simple_test_runner.py

# Run full tests
python3 -m pytest test_delete_truekey_logins.py -v
```

### Code Quality Checks
```bash
# Format code
black .

# Sort imports
isort .

# Check style
flake8 .

# Security scan
bandit -r .
```

## Workflow Configuration

### Environment Variables
- `TRUEKEY_EXTENSION_ID`: Extension ID for testing (default: "cpaibbcbodhimfnjnakiidgbpiehfgci")

### Caching
- Pip dependencies are cached to speed up builds
- Cache keys based on requirements files
- Automatic cache invalidation on dependency changes

### Artifacts
- **Unit Test Results**: Available for 7 days
- **Full Test Results**: Available for 30 days
- **Coverage Reports**: Available for 30 days
- **Security Reports**: Available for 30 days
- **Build Packages**: Available for 7 days

## Troubleshooting

### Common Issues

#### 1. Tests Failing on Different OS
- **Issue**: Tests pass on Ubuntu but fail on Windows/macOS
- **Solution**: Check OS-specific paths and dependencies
- **Prevention**: Test locally on multiple platforms

#### 2. Chrome/ChromeDriver Issues
- **Issue**: Selenium tests failing due to browser setup
- **Solution**: Ensure proper Chrome/ChromeDriver installation in CI
- **Prevention**: Use headless mode and proper browser setup

#### 3. Dependency Conflicts
- **Issue**: Package version conflicts between test dependencies
- **Solution**: Pin specific versions in requirements-test.txt
- **Prevention**: Regular dependency updates and testing

#### 4. Coverage Report Issues
- **Issue**: Coverage reports not generating or uploading
- **Solution**: Check pytest-cov configuration and file paths
- **Prevention**: Test coverage locally before pushing

### Debugging Workflows

#### View Logs
1. Go to the Actions tab in your GitHub repository
2. Click on the failed workflow run
3. Click on the failed job
4. Click on the failed step to view detailed logs

#### Local Reproduction
```bash
# Reproduce the exact CI environment
docker run -it --rm -v $(pwd):/workspace ubuntu:latest bash
cd /workspace
apt-get update && apt-get install -y python3 python3-pip
pip3 install -r requirements-test.txt
python3 -m pytest test_delete_truekey_logins.py -v
```

## Customization

### Adding New Tests
1. Add test functions to `test_delete_truekey_logins.py`
2. Update `simple_test_runner.py` if needed for basic tests
3. Tests will automatically run in both workflows

### Modifying Test Matrix
Edit the `strategy.matrix` section in workflow files:
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]
```

### Adding New Quality Checks
1. Install the tool in the workflow
2. Add the check step
3. Update local development script

## Performance Optimization

### Reducing CI Time
- Use dependency caching
- Exclude unnecessary matrix combinations
- Run expensive checks only on main branch
- Use parallel jobs where possible

### Cost Optimization
- Limit concurrent runs for private repositories
- Use smaller runners for basic tests
- Clean up artifacts regularly
- Optimize test execution time

## Security Considerations

### Secrets Management
- Use GitHub Secrets for sensitive data
- Never hardcode API keys or passwords
- Rotate secrets regularly
- Use least privilege principle

### Dependency Security
- Regular security scans with bandit and safety
- Keep dependencies updated
- Use dependency pinning
- Monitor for known vulnerabilities

## Monitoring and Alerts

### Status Notifications
- Workflow failures can trigger notifications
- Set up Slack/email alerts for critical failures
- Monitor coverage trends
- Track build performance metrics

### Metrics to Watch
- Test execution time
- Coverage percentage
- Failure rates
- Build success rate
- Security vulnerability count
