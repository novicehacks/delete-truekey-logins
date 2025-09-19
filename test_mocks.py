"""
Mock utilities for TrueKey Login Deleter Script tests

This module provides reusable mock objects and utilities for testing
the TrueKey deletion script functionality.
"""

import unittest.mock as mock
from unittest.mock import Mock, MagicMock
import tempfile
import os
import shutil


class MockChromeProfile:
    """Mock Chrome profile for testing"""
    
    def __init__(self, profile_path=None):
        self.profile_path = profile_path or tempfile.mkdtemp()
        self.default_path = os.path.join(self.profile_path, "Default")
        self.extensions_path = os.path.join(self.default_path, "Extensions")
        
        # Create mock profile structure
        os.makedirs(self.extensions_path, exist_ok=True)
        
        # Create mock files
        self.create_mock_files()
    
    def create_mock_files(self):
        """Create mock Chrome profile files"""
        # Mock preferences file
        preferences = {
            "profile": {
                "name": "Default"
            },
            "extensions": {
                "settings": {}
            }
        }
        
        import json
        with open(os.path.join(self.profile_path, "Preferences"), "w") as f:
            json.dump(preferences, f)
        
        # Mock local state file
        local_state = {
            "profile": {
                "info_cache": {
                    "Default": {
                        "name": "Default",
                        "user_name": "test_user"
                    }
                }
            }
        }
        
        with open(os.path.join(self.profile_path, "Local State"), "w") as f:
            json.dump(local_state, f)
    
    def cleanup(self):
        """Clean up the mock profile"""
        if os.path.exists(self.profile_path):
            shutil.rmtree(self.profile_path)


class MockWebDriver:
    """Mock Selenium WebDriver for testing"""
    
    def __init__(self):
        self.current_url = ""
        self.page_source = "<html><body>Mock page</body></html>"
        self.mock_elements = {}
        self.mock_find_calls = []
        self.mock_navigation_calls = []
    
    def get(self, url):
        """Mock navigation to URL"""
        self.current_url = url
        self.mock_navigation_calls.append(("get", url))
    
    def find_element(self, by, value):
        """Mock element finding"""
        self.mock_find_calls.append(("find_element", by, value))
        
        # Return mock element based on what we're looking for
        if by == "id" and value == "list-mode":
            return MockWebElement("list-mode-icon")
        elif "button" in str(value).lower() and ("yes" in str(value).lower() or "confirm" in str(value).lower()):
            return MockWebElement("confirm-button")
        else:
            return MockWebElement(f"mock-element-{value}")
    
    def find_elements(self, by, value):
        """Mock finding multiple elements"""
        self.mock_find_calls.append(("find_elements", by, value))
        
        # Return mock trash icons if looking for trash icons
        if "trash.svg" in str(value):
            # Simulate finding trash icons
            return [MockWebElement("trash-icon-1"), MockWebElement("trash-icon-2")]
        else:
            return []
    
    def quit(self):
        """Mock driver quit"""
        self.mock_navigation_calls.append(("quit", None))


class MockWebElement:
    """Mock Selenium WebElement for testing"""
    
    def __init__(self, element_id):
        self.element_id = element_id
        self.mock_clicks = 0
        self.is_displayed = True
        self.is_enabled = True
        self.text = f"Mock text for {element_id}"
    
    def click(self):
        """Mock element click"""
        self.mock_clicks += 1
    
    def is_displayed(self):
        """Mock display check"""
        return self.is_displayed
    
    def is_enabled(self):
        """Mock enabled check"""
        return self.is_enabled


class MockSubprocess:
    """Mock subprocess for testing Chrome process management"""
    
    def __init__(self, chrome_running=False):
        self.chrome_running = chrome_running
        self.mock_calls = []
    
    def run(self, args, **kwargs):
        """Mock subprocess run"""
        self.mock_calls.append((args, kwargs))
        
        # Mock Chrome process detection
        if "pgrep" in args and "Google Chrome" in args:
            mock_result = Mock()
            if self.chrome_running:
                mock_result.stdout = "12345\n67890\n"  # Mock running processes
            else:
                mock_result.stdout = ""  # No running processes
            mock_result.stderr = ""
            mock_result.returncode = 0
            return mock_result
        
        # Mock Chrome process termination
        elif "pkill" in args and "Google Chrome" in args:
            mock_result = Mock()
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_result.returncode = 0
            return mock_result
        
        # Default mock result
        mock_result = Mock()
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_result.returncode = 0
        return mock_result


class MockActionChains:
    """Mock Selenium ActionChains for testing"""
    
    def __init__(self, driver):
        self.driver = driver
        self.actions = []
    
    def move_to_element(self, element):
        """Mock move to element action"""
        self.actions.append(("move_to_element", element))
        return self
    
    def perform(self):
        """Mock perform actions"""
        self.actions.append(("perform", None))


def create_mock_truekey_environment():
    """Create a complete mock environment for testing"""
    return {
        "chrome_profile": MockChromeProfile(),
        "web_driver": MockWebDriver(),
        "subprocess": MockSubprocess(),
        "action_chains": MockActionChains
    }


def mock_extension_id_validation(extension_id):
    """Mock extension ID validation"""
    return (len(extension_id) == 32 and 
            extension_id.isalnum() and 
            extension_id.islower())


def create_mock_trash_icons(count=3):
    """Create mock trash icon elements"""
    return [MockWebElement(f"trash-icon-{i}") for i in range(1, count + 1)]


def create_mock_confirmation_dialog():
    """Create mock confirmation dialog elements"""
    return MockWebElement("confirm-button")


class MockChromeOptions:
    """Mock Chrome options for testing"""
    
    def __init__(self):
        self.arguments = []
    
    def add_argument(self, arg):
        """Mock adding Chrome argument"""
        self.arguments.append(arg)
    
    def add_experimental_option(self, name, value):
        """Mock adding experimental option"""
        self.arguments.append(f"--{name}={value}")


# Test data constants
DEFAULT_EXTENSION_ID = "cpaibbcbodhimfnjnakiidgbpiehfgci"
DEFAULT_DASHBOARD_URL = f"chrome-extension://{DEFAULT_EXTENSION_ID}/html/dashboard.html"

VALID_EXTENSION_IDS = [
    "cpaibbcbodhimfnjnakiidgbpiehfgci",
    "abcdefghijklmnopqrstuvwxyz123456",
    "1234567890abcdefghijklmnopqrstuv"
]

INVALID_EXTENSION_IDS = [
    "short",
    "ThisExtensionIDIsWayTooLongAndExceedsTheMaximumLengthOf32Characters",
    "CPAIBBCBODHIMFNJNAKIIDGBPIEHFGCI",
    "cpaibbcbodhimfnjnakiidgbpiehfgc-",
    "cpaibbcbodhimfnjnakiidgbpiehfgc ",
    ""
]

MOCK_CHROME_ARGUMENTS = [
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
