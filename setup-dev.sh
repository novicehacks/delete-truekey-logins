#!/bin/bash

# Development Setup Script for TrueKey Login Deleter
# This script sets up the development environment for local testing

set -e

echo "🚀 Setting up TrueKey Login Deleter development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is available
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Create virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements-test.txt
    print_success "Dependencies installed"
}

# Run basic tests
run_basic_tests() {
    print_status "Running basic tests..."
    python3 simple_test_runner.py
    print_success "Basic tests completed"
}

# Run full tests
run_full_tests() {
    print_status "Running full test suite..."
    python3 -m pytest test_delete_truekey_logins.py -v
    print_success "Full tests completed"
}

# Check code quality
check_code_quality() {
    print_status "Checking code quality..."
    
    # Install additional tools if not present
    pip install flake8 black isort bandit safety
    
    # Check formatting
    print_status "Checking code formatting..."
    black --check --diff . || print_warning "Code formatting issues found"
    
    # Check imports
    print_status "Checking import sorting..."
    isort --check-only --diff . || print_warning "Import sorting issues found"
    
    # Check style
    print_status "Checking code style..."
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || print_warning "Code style issues found"
    
    # Security scan
    print_status "Running security scan..."
    bandit -r . || print_warning "Security issues found"
    
    print_success "Code quality check completed"
}

# Main execution
main() {
    echo "=========================================="
    echo "TrueKey Login Deleter - Development Setup"
    echo "=========================================="
    
    check_python
    setup_venv
    install_dependencies
    
    echo ""
    echo "=========================================="
    echo "Running Tests..."
    echo "=========================================="
    
    run_basic_tests
    
    echo ""
    echo "=========================================="
    echo "Code Quality Checks..."
    echo "=========================================="
    
    check_code_quality
    
    echo ""
    echo "=========================================="
    echo "Development Setup Complete! 🎉"
    echo "=========================================="
    echo ""
    echo "Available commands:"
    echo "  source venv/bin/activate    # Activate virtual environment"
    echo "  python3 simple_test_runner.py    # Run basic tests"
    echo "  python3 -m pytest test_delete_truekey_logins.py -v    # Run full tests"
    echo "  python3 run_tests.py --coverage    # Run tests with coverage"
    echo "  python3 delete-truekey-logins.py    # Run the main script"
    echo ""
    echo "To run full tests with coverage:"
    echo "  python3 -m pytest test_delete_truekey_logins.py --cov=. --cov-report=html"
    echo ""
}

# Run main function
main "$@"
