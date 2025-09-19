#!/usr/bin/env python3
"""
Test runner script for TrueKey Login Deleter Script

This script provides an easy way to run the test suite with various options
and configurations.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit            # Run only unit tests
    python run_tests.py --integration     # Run only integration tests
    python run_tests.py --coverage        # Run tests with coverage report
    python run_tests.py --verbose         # Run with verbose output
"""

import sys
import subprocess
import argparse
import os


def run_tests(test_type=None, coverage=False, verbose=False, markers=None):
    """
    Run the test suite with specified options.
    
    Args:
        test_type (str): Type of tests to run ('unit', 'integration', 'all')
        coverage (bool): Whether to generate coverage report
        verbose (bool): Whether to use verbose output
        markers (list): List of pytest markers to filter tests
    
    Returns:
        int: Exit code from pytest
    """
    cmd = ["python", "-m", "pytest"]
    
    # Add test file
    cmd.append("test_delete_truekey_logins.py")
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    # Add verbose output
    if verbose:
        cmd.append("-vv")
    
    # Add markers if specified
    if markers:
        marker_expr = " or ".join(markers)
        cmd.extend(["-m", marker_expr])
    
    # Add test type filtering
    if test_type == "unit":
        cmd.extend(["-k", "test_chrome_process or test_setup_truekey_profile or test_extension_id"])
    elif test_type == "integration":
        cmd.extend(["-k", "test_complete_workflow"])
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: pytest not found. Please install test dependencies:")
        print("pip install -r requirements-test.txt")
        return 1


def check_dependencies():
    """Check if required test dependencies are installed."""
    required_packages = ["pytest", "selenium"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall with: pip install -r requirements-test.txt")
        print("\nAlternatively, you can run basic tests without pytest:")
        print("  python3 test_delete_truekey_logins.py")
        return False
    
    return True


def main():
    """Main function to handle command line arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run TrueKey Login Deleter Script tests")
    
    parser.add_argument("--unit", action="store_true", 
                       help="Run only unit tests")
    parser.add_argument("--integration", action="store_true",
                       help="Run only integration tests")
    parser.add_argument("--coverage", action="store_true",
                       help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--markers", nargs="+",
                       help="Pytest markers to filter tests")
    parser.add_argument("--check-deps", action="store_true",
                       help="Check if test dependencies are installed")
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps:
        if check_dependencies():
            print("All required dependencies are installed.")
            return 0
        else:
            return 1
    
    # Check dependencies before running tests
    if not check_dependencies():
        return 1
    
    # Determine test type
    test_type = None
    if args.unit:
        test_type = "unit"
    elif args.integration:
        test_type = "integration"
    else:
        test_type = "all"
    
    # Run tests
    exit_code = run_tests(
        test_type=test_type,
        coverage=args.coverage,
        verbose=args.verbose,
        markers=args.markers
    )
    
    # Print summary
    print("=" * 60)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")
    
    # Print coverage report location if generated
    if args.coverage and exit_code == 0:
        print("\n📊 Coverage report generated:")
        print("   HTML report: htmlcov/index.html")
        print("   Terminal report: see output above")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
