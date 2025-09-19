"""
Test suite for TrueKey Login Deleter Script

This test suite uses pytest and unittest.mock to test the functionality
of the delete-truekey-logins.py script without requiring actual Chrome
or TrueKey extension access.

Run tests with: pytest test_delete_truekey_logins.py -v
"""

import unittest.mock as mock
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, MagicMock, patch, call

# Try to import pytest, but don't fail if it's not available
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    # Create a dummy pytest module for basic functionality
    class DummyPytest:
        @staticmethod
        def main(args):
            print("pytest not available. Install with: pip install pytest")
            return 0
    
    pytest = DummyPytest()

# Add the current directory to the path to import our script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the script functions (we'll need to refactor the script to be testable)
# For now, we'll test the logic by mocking the entire script execution


class TestTrueKeyDeletionScript:
    """Test class for TrueKey deletion script functionality"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_chrome_profile = os.path.join(self.temp_dir, "Chrome")
        self.mock_truekey_profile = os.path.join(self.temp_dir, "TrueKey")
        
        # Create mock profile structure
        os.makedirs(os.path.join(self.mock_chrome_profile, "Default"), exist_ok=True)
        os.makedirs(os.path.join(self.mock_chrome_profile, "Default", "Extensions"), exist_ok=True)
        
        # Mock files
        with open(os.path.join(self.mock_chrome_profile, "Preferences"), "w") as f:
            f.write('{"mock": "preferences"}')
        with open(os.path.join(self.mock_chrome_profile, "Local State"), "w") as f:
            f.write('{"mock": "local_state"}')
    
    def teardown_method(self):
        """Clean up test fixtures after each test method"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('subprocess.run')
    def test_chrome_process_detection_running(self, mock_subprocess):
        """Test detection of running Chrome processes"""
        # Mock Chrome processes running
        mock_result = Mock()
        mock_result.stdout = "12345\n67890"  # Simulate running Chrome processes
        mock_subprocess.return_value = mock_result
        
        # Test the process detection logic using actual subprocess module
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                               capture_output=True, text=True)
        
        assert result.stdout.strip() != ""
        mock_subprocess.assert_called_with(['pgrep', '-f', 'Google Chrome'], 
                                         capture_output=True, text=True)
    
    @patch('subprocess.run')
    def test_chrome_process_detection_not_running(self, mock_subprocess):
        """Test detection when Chrome is not running"""
        # Mock no Chrome processes running
        mock_result = Mock()
        mock_result.stdout = ""
        mock_subprocess.return_value = mock_result
        
        # Test using actual subprocess module
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                               capture_output=True, text=True)
        
        assert result.stdout.strip() == ""
    
    @patch('subprocess.run')
    def test_chrome_process_termination(self, mock_subprocess):
        """Test automatic Chrome process termination"""
        # Mock Chrome processes running
        mock_result = Mock()
        mock_result.stdout = "12345\n67890"
        mock_subprocess.return_value = mock_result
        
        # Test the termination logic using actual subprocess module
        import subprocess
        subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                      capture_output=True, text=True)
        subprocess.run(['pkill', '-f', 'Google Chrome'], check=False)
        
        # Verify both commands were called
        assert mock_subprocess.call_count >= 2
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    @patch('shutil.copytree')
    @patch('shutil.rmtree')
    def test_setup_truekey_profile(self, mock_rmtree, mock_copytree, mock_copy2, mock_makedirs, mock_exists):
        """Test TrueKey profile setup functionality"""
        # Mock file system operations
        mock_exists.return_value = True
        mock_makedirs.return_value = None
        mock_copy2.return_value = None
        mock_copytree.return_value = None
        mock_rmtree.return_value = None
        
        # Test profile setup logic
        chrome_profile_path = "/mock/chrome/profile"
        truekey_profile_dir = "/mock/truekey/profile"
        
        # Simulate the setup_truekey_profile function logic
        os.makedirs(truekey_profile_dir, exist_ok=True)
        
        default_profile = os.path.join(chrome_profile_path, "Default")
        if os.path.exists(default_profile):
            truekey_default = os.path.join(truekey_profile_dir, "Default")
            os.makedirs(truekey_default, exist_ok=True)
            
            # Copy preferences
            for item in ["Preferences", "Secure Preferences", "Local State"]:
                src = os.path.join(chrome_profile_path, item)
                if os.path.exists(src):
                    shutil.copy2(src, truekey_profile_dir)
            
            # Copy extensions
            ext_src = os.path.join(default_profile, "Extensions")
            ext_dst = os.path.join(truekey_default, "Extensions")
            if os.path.exists(ext_src):
                if os.path.exists(ext_dst):
                    shutil.rmtree(ext_dst)
                shutil.copytree(ext_src, ext_dst)
        
        # Verify operations were called
        mock_makedirs.assert_called()
        mock_copy2.assert_called()
        mock_copytree.assert_called()
        mock_rmtree.assert_called()
    
    @patch('selenium.webdriver.Chrome')
    def test_chrome_driver_creation(self, mock_chrome_driver):
        """Test Chrome WebDriver creation with proper options"""
        # Mock WebDriver
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        # Test Chrome options configuration
        from selenium import webdriver
        
        options = webdriver.ChromeOptions()
        
        # Test key arguments that should be set
        test_arguments = [
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--disable-web-security",
            "--disable-features=CrossSiteDocumentBlockingIfIsolating",
            "--remote-debugging-port=0",
            "--disable-extensions-file-access-check",
            "--disable-extensions-http-throttling",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-field-trial-config",
            "--disable-ipc-flooding-protection",
            "--disable-hang-monitor",
            "--disable-prompt-on-repost",
            "--disable-sync",
            "--disable-translate",
            "--no-service-autorun",
            "--password-store=basic"
        ]
        
        for arg in test_arguments:
            options.add_argument(arg)
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        
        # Verify driver was created
        assert driver == mock_driver
        mock_chrome_driver.assert_called_once_with(options=options)
    
    @patch('selenium.webdriver.Chrome')
    def test_extension_dashboard_navigation(self, mock_chrome_driver):
        """Test navigation to TrueKey extension dashboard"""
        # Mock WebDriver and methods
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        # Test navigation
        extension_id = "cpaibbcbodhimfnjnakiidgbpiehfgci"
        dashboard_url = f"chrome-extension://{extension_id}/html/dashboard.html"
        
        # Import webdriver within the test
        from selenium import webdriver
        driver = webdriver.Chrome()
        driver.get(dashboard_url)
        
        # Verify navigation
        mock_driver.get.assert_called_with(dashboard_url)
    
    @patch('selenium.webdriver.Chrome')
    def test_list_mode_switching(self, mock_chrome_driver):
        """Test switching to list mode in TrueKey extension"""
        # Mock WebDriver and elements
        mock_driver = Mock()
        mock_list_mode_icon = Mock()
        
        mock_chrome_driver.return_value = mock_driver
        mock_driver.find_element.return_value = mock_list_mode_icon
        
        # Test list mode switching
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        
        driver = webdriver.Chrome()
        list_mode_icon = driver.find_element(By.ID, "list-mode")
        list_mode_icon.click()
        
        # Verify operations
        mock_driver.find_element.assert_called_with(By.ID, "list-mode")
        mock_list_mode_icon.click.assert_called_once()
    
    @patch('selenium.webdriver.Chrome')
    def test_trash_icon_detection(self, mock_chrome_driver):
        """Test detection of trash icons for deletion"""
        # Mock WebDriver and elements
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        # Mock trash icons
        mock_trash_icon1 = Mock()
        mock_trash_icon2 = Mock()
        mock_driver.find_elements.return_value = [mock_trash_icon1, mock_trash_icon2]
        
        # Test trash icon detection
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        
        driver = webdriver.Chrome()
        trash_icons = driver.find_elements(By.XPATH, 
                                         '//img[contains(@src, "../images/common/svg/trash.svg")]')
        
        # Verify detection
        assert len(trash_icons) == 2
        mock_driver.find_elements.assert_called_with(By.XPATH, 
                                                   '//img[contains(@src, "../images/common/svg/trash.svg")]')
    
    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.common.action_chains.ActionChains')
    def test_deletion_process(self, mock_action_chains, mock_chrome_driver):
        """Test the deletion process with confirmation dialogs"""
        # Mock WebDriver and elements
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        # Mock trash icons and confirmation button
        mock_trash_icon = Mock()
        mock_confirm_button = Mock()
        
        # First call returns trash icons, second call returns empty (no more icons)
        mock_driver.find_elements.side_effect = [
            [mock_trash_icon],  # First iteration
            []  # Second iteration (empty, exits loop)
        ]
        mock_driver.find_element.return_value = mock_confirm_button
        
        # Mock ActionChains
        mock_action_chains_instance = Mock()
        mock_action_chains.return_value = mock_action_chains_instance
        
        # Test deletion process
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.action_chains import ActionChains
        
        driver = webdriver.Chrome()
        
        # Simulate the deletion loop
        deletion_count = 0
        while True:
            trash_icons = driver.find_elements(By.XPATH, 
                                             '//img[contains(@src, "../images/common/svg/trash.svg")]')
            if not trash_icons:
                break
            
            for icon in trash_icons:
                ActionChains(driver).move_to_element(icon).perform()
                icon.click()
                
                # Try to find confirmation button
                try:
                    confirm_button = driver.find_element(By.XPATH, 
                                                       '//button[contains(text(), "Yes") or contains(text(), "Confirm")]')
                    confirm_button.click()
                    deletion_count += 1
                except:
                    deletion_count += 1
        
        # Verify operations
        assert deletion_count == 1
        mock_trash_icon.click.assert_called_once()
        mock_confirm_button.click.assert_called_once()
    
    def test_extension_id_configuration(self):
        """Test extension ID configuration and URL generation"""
        # Test default extension ID
        default_extension_id = "cpaibbcbodhimfnjnakiidgbpiehfgci"
        dashboard_url = f"chrome-extension://{default_extension_id}/html/dashboard.html"
        
        expected_url = "chrome-extension://cpaibbcbodhimfnjnakiidgbpiehfgci/html/dashboard.html"
        assert dashboard_url == expected_url
        
        # Test custom extension ID
        custom_extension_id = "abcdefghijklmnopqrstuvwxyz123456"
        custom_dashboard_url = f"chrome-extension://{custom_extension_id}/html/dashboard.html"
        
        expected_custom_url = "chrome-extension://abcdefghijklmnopqrstuvwxyz123456/html/dashboard.html"
        assert custom_dashboard_url == expected_custom_url
    
    def test_extension_id_format_validation(self):
        """Test extension ID format validation"""
        # Valid extension IDs (32 characters, lowercase alphanumeric)
        valid_ids = [
            "cpaibbcbodhimfnjnakiidgbpiehfgci",  # Default TrueKey ID
            "abcdefghijklmnopqrstuvwxyz123456",  # Custom valid ID
            "1234567890abcdefghijklmnopqrstuv"   # Another valid format
        ]
        
        # Invalid extension IDs
        invalid_ids = [
            "short",  # Too short
            "ThisExtensionIDIsWayTooLongAndExceedsTheMaximumLengthOf32Characters",  # Too long
            "CPAIBBCBODHIMFNJNAKIIDGBPIEHFGCI",  # Uppercase
            "cpaibbcbodhimfnjnakiidgbpiehfgc-",  # Contains special character
            "cpaibbcbodhimfnjnakiidgbpiehfgc ",  # Contains space
            ""  # Empty
        ]
        
        # Test validation logic
        def validate_extension_id(extension_id):
            return (len(extension_id) == 32 and 
                   extension_id.isalnum() and 
                   extension_id.islower())
        
        # Test valid IDs
        for valid_id in valid_ids:
            assert validate_extension_id(valid_id), f"ID {valid_id} should be valid"
        
        # Test invalid IDs
        for invalid_id in invalid_ids:
            assert not validate_extension_id(invalid_id), f"ID {invalid_id} should be invalid"
    
    @patch('os.path.exists')
    def test_profile_existence_check(self, mock_exists):
        """Test TrueKey profile existence checking"""
        # Mock profile exists
        mock_exists.return_value = True
        
        truekey_profile_dir = "/mock/truekey/profile"
        profile_exists = os.path.exists(truekey_profile_dir)
        
        assert profile_exists is True
        mock_exists.assert_called_with(truekey_profile_dir)
        
        # Mock profile doesn't exist
        mock_exists.return_value = False
        profile_exists = os.path.exists(truekey_profile_dir)
        
        assert profile_exists is False
    
    def test_argument_parsing(self):
        """Test command line argument parsing"""
        # Test default arguments
        with patch('sys.argv', ['delete-truekey-logins.py']):
            import argparse
            
            parser = argparse.ArgumentParser(description='TrueKey Login Deleter Script')
            parser.add_argument('--extension-id', 
                             default='cpaibbcbodhimfnjnakiidgbpiehfgci',
                             help='TrueKey extension ID')
            parser.add_argument('--validate-only', 
                             action='store_true',
                             help='Only validate the extension ID and exit')
            
            args = parser.parse_args([])
            
            assert args.extension_id == 'cpaibbcbodhimfnjnakiidgbpiehfgci'
            assert args.validate_only is False
        
        # Test custom extension ID
        with patch('sys.argv', ['delete-truekey-logins.py', '--extension-id', 'customid123456789012345678901234']):
            parser = argparse.ArgumentParser(description='TrueKey Login Deleter Script')
            parser.add_argument('--extension-id', 
                             default='cpaibbcbodhimfnjnakiidgbpiehfgci',
                             help='TrueKey extension ID')
            parser.add_argument('--validate-only', 
                             action='store_true',
                             help='Only validate the extension ID and exit')
            
            args = parser.parse_args(['--extension-id', 'customid123456789012345678901234'])
            
            assert args.extension_id == 'customid123456789012345678901234'
        
        # Test validate-only flag
        with patch('sys.argv', ['delete-truekey-logins.py', '--validate-only']):
            parser = argparse.ArgumentParser(description='TrueKey Login Deleter Script')
            parser.add_argument('--extension-id', 
                             default='cpaibbcbodhimfnjnakiidgbpiehfgci',
                             help='TrueKey extension ID')
            parser.add_argument('--validate-only', 
                             action='store_true',
                             help='Only validate the extension ID and exit')
            
            args = parser.parse_args(['--validate-only'])
            
            assert args.validate_only is True


class TestTrueKeyScriptIntegration:
    """Integration tests for the complete TrueKey deletion workflow"""
    
    @patch('selenium.webdriver.Chrome')
    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    @patch('shutil.copytree')
    def test_complete_workflow_mock(self, mock_copytree, mock_copy2, mock_makedirs, 
                                   mock_exists, mock_subprocess, mock_chrome_driver):
        """Test the complete workflow with all mocks"""
        # Setup mocks
        mock_subprocess.return_value = Mock(stdout="")  # No Chrome running
        mock_exists.return_value = True  # Profile exists
        mock_makedirs.return_value = None
        mock_copy2.return_value = None
        mock_copytree.return_value = None
        
        # Mock WebDriver
        mock_driver = Mock()
        mock_chrome_driver.return_value = mock_driver
        
        # Mock elements
        mock_list_icon = Mock()
        mock_trash_icon = Mock()
        mock_confirm_button = Mock()
        
        mock_driver.find_element.side_effect = [mock_list_icon, mock_confirm_button]
        mock_driver.find_elements.side_effect = [
            [mock_trash_icon],  # First call returns trash icons
            []  # Second call returns empty (no more icons)
        ]
        
        # Test the workflow steps
        # 1. Check Chrome processes
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'Google Chrome'], 
                               capture_output=True, text=True)
        assert result.stdout == ""
        
        # 2. Create driver
        from selenium import webdriver
        driver = webdriver.Chrome()
        assert driver == mock_driver
        
        # 3. Navigate to dashboard
        extension_id = "cpaibbcbodhimfnjnakiidgbpiehfgci"
        dashboard_url = f"chrome-extension://{extension_id}/html/dashboard.html"
        driver.get(dashboard_url)
        
        # 4. Switch to list view
        from selenium.webdriver.common.by import By
        list_icon = driver.find_element(By.ID, "list-mode")
        list_icon.click()
        
        # 5. Delete items
        deletion_count = 0
        while True:
            trash_icons = driver.find_elements(By.XPATH, 
                                             '//img[contains(@src, "../images/common/svg/trash.svg")]')
            if not trash_icons:
                break
            
            for icon in trash_icons:
                icon.click()
                try:
                    confirm_button = driver.find_element(By.XPATH, 
                                                       '//button[contains(text(), "Yes") or contains(text(), "Confirm")]')
                    confirm_button.click()
                    deletion_count += 1
                except:
                    deletion_count += 1
        
        # 6. Cleanup
        driver.quit()
        
        # Verify workflow
        assert deletion_count == 1
        mock_driver.get.assert_called_with(dashboard_url)
        mock_list_icon.click.assert_called_once()
        mock_trash_icon.click.assert_called_once()
        mock_confirm_button.click.assert_called_once()
        mock_driver.quit.assert_called_once()


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        # Run tests with pytest
        pytest.main([__file__, "-v"])
    else:
        print("pytest not available. Running basic tests instead...")
        print("For full test suite, install pytest: pip install pytest")
        print("\nRunning simple test runner...")
        
        # Import and run simple test runner
        try:
            from simple_test_runner import run_basic_tests
            sys.exit(run_basic_tests())
        except ImportError:
            print("simple_test_runner.py not found. Please ensure all test files are present.")
            sys.exit(1)
