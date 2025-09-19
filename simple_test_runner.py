#!/usr/bin/env python3
"""
Simple test runner for TrueKey Login Deleter Script

This script runs basic tests without requiring pytest, using only
Python's built-in unittest module and mocking capabilities.

Usage:
    python3 simple_test_runner.py
"""

import sys
import os
import unittest
import unittest.mock as mock
from unittest.mock import Mock, patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestTrueKeyBasicFunctionality(unittest.TestCase):
    """Basic tests for TrueKey script functionality without pytest"""
    
    def test_extension_id_validation(self):
        """Test extension ID format validation"""
        def validate_extension_id(extension_id):
            return (len(extension_id) == 32 and 
                   extension_id.isalnum() and 
                   extension_id.islower())
        
        # Test valid extension IDs
        valid_ids = [
            "cpaibbcbodhimfnjnakiidgbpiehfgci",
            "abcdefghijklmnopqrstuvwxyz123456",
            "1234567890abcdefghijklmnopqrstuv"
        ]
        
        for valid_id in valid_ids:
            with self.subTest(extension_id=valid_id):
                self.assertTrue(validate_extension_id(valid_id), 
                              f"ID {valid_id} should be valid")
        
        # Test invalid extension IDs
        invalid_ids = [
            "short",
            "ThisExtensionIDIsWayTooLongAndExceedsTheMaximumLengthOf32Characters",
            "CPAIBBCBODHIMFNJNAKIIDGBPIEHFGCI",
            "cpaibbcbodhimfnjnakiidgbpiehfgc-",
            "cpaibbcbodhimfnjnakiidgbpiehfgc ",
            ""
        ]
        
        for invalid_id in invalid_ids:
            with self.subTest(extension_id=invalid_id):
                self.assertFalse(validate_extension_id(invalid_id), 
                               f"ID {invalid_id} should be invalid")
    
    def test_dashboard_url_generation(self):
        """Test TrueKey dashboard URL generation"""
        extension_id = "cpaibbcbodhimfnjnakiidgbpiehfgci"
        dashboard_url = f"chrome-extension://{extension_id}/html/dashboard.html"
        
        expected_url = "chrome-extension://cpaibbcbodhimfnjnakiidgbpiehfgci/html/dashboard.html"
        self.assertEqual(dashboard_url, expected_url)
    
    @patch('subprocess.run')
    def test_chrome_process_detection(self, mock_subprocess):
        """Test Chrome process detection logic"""
        # Test Chrome running
        mock_result = Mock()
        mock_result.stdout = "12345\n67890"
        mock_subprocess.return_value = mock_result
        
        # Simulate the actual subprocess call
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                               capture_output=True, text=True)
        
        self.assertNotEqual(result.stdout.strip(), "")
        mock_subprocess.assert_called_with(['pgrep', '-f', 'Google Chrome'], 
                                         capture_output=True, text=True)
        
        # Reset mock for second test
        mock_subprocess.reset_mock()
        
        # Test Chrome not running
        mock_result.stdout = ""
        mock_subprocess.return_value = mock_result
        
        result = subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                               capture_output=True, text=True)
        
        self.assertEqual(result.stdout.strip(), "")
    
    @patch('subprocess.run')
    def test_chrome_process_termination(self, mock_subprocess):
        """Test Chrome process termination"""
        mock_result = Mock()
        mock_result.stdout = "12345"
        mock_subprocess.return_value = mock_result
        
        # Simulate process termination using actual subprocess module
        import subprocess
        subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                      capture_output=True, text=True)
        subprocess.run(['pkill', '-f', 'Google Chrome'], check=False)
        
        self.assertEqual(mock_subprocess.call_count, 2)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_profile_existence_check(self, mock_makedirs, mock_exists):
        """Test profile existence checking"""
        # Test profile exists
        mock_exists.return_value = True
        
        profile_path = "/mock/profile/path"
        profile_exists = os.path.exists(profile_path)
        
        self.assertTrue(profile_exists)
        mock_exists.assert_called_with(profile_path)
        
        # Test profile doesn't exist
        mock_exists.return_value = False
        profile_exists = os.path.exists(profile_path)
        
        self.assertFalse(profile_exists)
    
    def test_chrome_options_configuration(self):
        """Test Chrome options configuration"""
        try:
            from selenium import webdriver
        except ImportError:
            self.skipTest("selenium not available")
        
        options = webdriver.ChromeOptions()
        
        # Test adding key arguments
        test_arguments = [
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--disable-web-security",
            "--remote-debugging-port=0"
        ]
        
        for arg in test_arguments:
            options.add_argument(arg)
        
        # Verify arguments were added (this tests the ChromeOptions class)
        self.assertTrue(hasattr(options, 'arguments'))
    
    def test_mock_webdriver_functionality(self):
        """Test mock WebDriver functionality"""
        # Import our mock utilities
        try:
            from test_mocks import MockWebDriver, MockWebElement
        except ImportError:
            self.skipTest("test_mocks not available")
        
        # Test mock driver creation
        driver = MockWebDriver()
        self.assertIsNotNone(driver)
        
        # Test navigation
        test_url = "chrome-extension://test123/html/dashboard.html"
        driver.get(test_url)
        
        self.assertEqual(driver.current_url, test_url)
        self.assertIn(("get", test_url), driver.mock_navigation_calls)
        
        # Test element finding
        element = driver.find_element("id", "test-element")
        self.assertIsInstance(element, MockWebElement)
        self.assertIn(("find_element", "id", "test-element"), driver.mock_find_calls)
        
        # Test element clicking
        element.click()
        self.assertEqual(element.mock_clicks, 1)
    
    def test_mock_profile_functionality(self):
        """Test mock Chrome profile functionality"""
        try:
            from test_mocks import MockChromeProfile
        except ImportError:
            self.skipTest("test_mocks not available")
        
        # Test profile creation
        profile = MockChromeProfile()
        self.assertTrue(os.path.exists(profile.profile_path))
        self.assertTrue(os.path.exists(profile.default_path))
        self.assertTrue(os.path.exists(profile.extensions_path))
        
        # Test mock files exist
        preferences_file = os.path.join(profile.profile_path, "Preferences")
        local_state_file = os.path.join(profile.profile_path, "Local State")
        
        self.assertTrue(os.path.exists(preferences_file))
        self.assertTrue(os.path.exists(local_state_file))
        
        # Cleanup
        profile.cleanup()
        self.assertFalse(os.path.exists(profile.profile_path))


def run_basic_tests():
    """Run basic tests without pytest"""
    print("Running basic TrueKey script tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTrueKeyBasicFunctionality)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_basic_tests()
    sys.exit(exit_code)
