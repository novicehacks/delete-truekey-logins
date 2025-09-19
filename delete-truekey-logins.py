"""
TrueKey Login Deleter Script

This script automates the deletion of all login entries in the TrueKey Chrome extension
by navigating to the extension dashboard, switching to list view, and systematically
clicking all trash icons to delete login entries.

Features:
- Automatic Chrome process management
- Dedicated TrueKey profile creation and management
- Configurable extension ID support
- User verification pause for safety
- Comprehensive error handling and cleanup

IMPORTANT: Before running this script:
1. Close ALL Chrome browser windows and processes completely
2. Wait 2-3 seconds after closing Chrome
3. Then run this script

This ensures the Chrome profile isn't locked by another instance.

Usage:
    python3 delete-truekey-logins.py [--extension-id EXTENSION_ID] [--validate-only]

Arguments:
    --extension-id: Custom TrueKey extension ID (default: cpaibbcbodhimfnjnakiidgbpiehfgci)
    --validate-only: Display extension ID and instructions without running the script

Environment Variables:
    TRUEKEY_EXTENSION_ID: Alternative way to specify extension ID

Author: NoviceHacks
License: MIT
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import tempfile
import sys
import argparse

# --- Configuration ---
# Parse command line arguments and environment variables
# This section handles user input for extension ID configuration and validation
parser = argparse.ArgumentParser(description='TrueKey Login Deleter Script')
parser.add_argument('--extension-id', 
                   default=os.environ.get('TRUEKEY_EXTENSION_ID', 'cpaibbcbodhimfnjnakiidgbpiehfgci'),
                   help='TrueKey extension ID (default: cpaibbcbodhimfnjnakiidgbpiehfgci)')
parser.add_argument('--validate-only', 
                   action='store_true',
                   help='Only validate the extension ID and exit')
args = parser.parse_args()

# TrueKey extension configuration
TRUEKEY_EXTENSION_ID = args.extension_id
TRUEKEY_DASHBOARD_URL = f"chrome-extension://{TRUEKEY_EXTENSION_ID}/html/dashboard.html"

print(f"Using TrueKey extension ID: {TRUEKEY_EXTENSION_ID}")
print(f"Dashboard URL: {TRUEKEY_DASHBOARD_URL}")

# Use your existing Chrome profile to access the TrueKey extension
import getpass
username = getpass.getuser()  # Gets current username dynamically
chrome_profile_path = f"/Users/{username}/Library/Application Support/Google/Chrome"

# TrueKey profile directory (permanent location for the copied profile)
truekey_profile_dir = f"/Users/{username}/Library/Application Support/Google/Chrome/TrueKey"

# --- Chrome Process Management ---
# Check if Chrome is running and attempt to close it automatically
# This prevents profile lock conflicts when starting the automation
import subprocess
try:
    result = subprocess.run(['pgrep', '-f', 'Google Chrome'], capture_output=True, text=True)
    if result.stdout.strip():
        print("WARNING: Chrome appears to be running.")
        print("Attempting to close Chrome processes...")
        
        # Try to kill Chrome processes using pkill command
        try:
            subprocess.run(['pkill', '-f', 'Google Chrome'], check=False)
            print("Chrome processes terminated.")
            time.sleep(3)  # Wait for processes to fully terminate
        except Exception:
            print("Could not automatically close Chrome. Please close ALL Chrome windows manually.")
            time.sleep(5)
            
except Exception:
    pass  # pgrep not available or other error, continue anyway

# --- Selenium Setup ---
def setup_truekey_profile():
    """
    Setup or update the TrueKey profile from the main Chrome profile.
    
    This function creates a dedicated TrueKey profile by copying essential files
    from the user's main Chrome profile. This includes preferences, settings,
    and the extensions directory to ensure the TrueKey extension is available
    in the isolated profile.
    
    The copied profile allows the script to run without interfering with the
    user's main Chrome instance while preserving all necessary TrueKey data.
    
    Returns:
        None
        
    Raises:
        OSError: If there are issues creating directories or copying files
        Exception: If the default Chrome profile is not found
        
    Note:
        This function creates a permanent TrueKey profile directory that will
        be reused in subsequent script runs for faster startup.
    """
    import shutil
    
    print("Setting up TrueKey profile...")
    
    # Create TrueKey profile directory
    os.makedirs(truekey_profile_dir, exist_ok=True)
    
    # Copy essential profile files
    default_profile = os.path.join(chrome_profile_path, "Default")
    if os.path.exists(default_profile):
        truekey_default = os.path.join(truekey_profile_dir, "Default")
        os.makedirs(truekey_default, exist_ok=True)
        
        # Copy preferences and settings
        for item in ["Preferences", "Secure Preferences", "Local State"]:
            src = os.path.join(chrome_profile_path, item)
            if os.path.exists(src):
                shutil.copy2(src, truekey_profile_dir)
        
        # Copy extensions directory (this preserves the TrueKey extension)
        ext_src = os.path.join(default_profile, "Extensions")
        ext_dst = os.path.join(truekey_default, "Extensions")
        
        if os.path.exists(ext_src):
            # Remove existing extensions directory if it exists
            if os.path.exists(ext_dst):
                shutil.rmtree(ext_dst)
            shutil.copytree(ext_src, ext_dst)
            print("Extensions copied successfully.")
        else:
            print("Warning: Extensions directory not found.")
        
        print("TrueKey profile setup complete.")
    else:
        print("Error: Default Chrome profile not found.")

def create_chrome_driver():
    """
    Create and configure a Chrome WebDriver instance for TrueKey automation.
    
    This function sets up a Chrome WebDriver with a dedicated TrueKey profile
    that contains the necessary extensions and settings. It automatically
    creates the profile if it doesn't exist and configures Chrome with
    specific options optimized for extension automation.
    
    The function uses multiple Chrome arguments to:
    - Disable security features that might block extension access
    - Prevent user prompts and dialogs that could interrupt automation
    - Optimize performance for automated operations
    - Ensure reliable extension communication
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
        
    Raises:
        Exception: If Chrome driver creation fails or Chrome is not properly installed
        
    Note:
        The function will automatically create the TrueKey profile on first run
        and reuse it in subsequent runs for faster startup.
        
    Chrome Options Configured:
        - Profile management (user-data-dir, profile-directory)
        - Security bypasses (disable-web-security, disable-features)
        - Extension access (disable-extensions-file-access-check)
        - Performance optimizations (disable-background-timer-throttling)
        - User experience (disable-sync, disable-translate, etc.)
    """
    
    # Check if TrueKey profile exists, if not create it
    if not os.path.exists(truekey_profile_dir):
        print("TrueKey profile not found. Creating it now...")
        setup_truekey_profile()
    else:
        print("Using existing TrueKey profile.")
    
    print("Creating Chrome driver with TrueKey profile...")
    
    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        
        # Profile and Directory Options
        options.add_argument(f"--user-data-dir={truekey_profile_dir}")  # Use our dedicated TrueKey profile
        options.add_argument("--profile-directory=Default")  # Use the Default profile within our data directory
        
        # Startup Behavior Options
        options.add_argument("--no-first-run")  # Skip first-run setup dialogs that could interfere with automation
        options.add_argument("--no-default-browser-check")  # Prevent Chrome from checking if it's the default browser
        options.add_argument("--disable-default-apps")  # Disable default Chrome apps that might interfere
        
        # Security and Extension Options
        options.add_argument("--disable-web-security")  # Allow access to extension pages and cross-origin requests
        options.add_argument("--disable-features=CrossSiteDocumentBlockingIfIsolating")  # Prevent blocking of extension content
        options.add_argument("--disable-extensions-file-access-check")  # Allow extensions to access local files
        options.add_argument("--disable-extensions-http-throttling")  # Prevent throttling of extension HTTP requests
        
        # Debugging and Port Options
        options.add_argument("--remote-debugging-port=0")  # Let Chrome automatically choose an available debugging port
        
        # Performance and Background Process Options
        options.add_argument("--disable-background-timer-throttling")  # Prevent throttling of background processes
        options.add_argument("--disable-backgrounding-occluded-windows")  # Keep windows active even when not visible
        options.add_argument("--disable-renderer-backgrounding")  # Prevent renderer processes from being backgrounded
        options.add_argument("--disable-field-trial-config")  # Disable field trials that could affect behavior
        options.add_argument("--disable-ipc-flooding-protection")  # Allow rapid IPC communication needed for automation
        
        # User Experience Options
        options.add_argument("--disable-hang-monitor")  # Prevent hang detection that could interrupt automation
        options.add_argument("--disable-prompt-on-repost")  # Disable repost confirmation dialogs
        options.add_argument("--disable-sync")  # Disable Chrome sync to avoid authentication prompts
        options.add_argument("--disable-translate")  # Disable translation prompts that could interfere
        options.add_argument("--no-service-autorun")  # Prevent automatic service startup
        options.add_argument("--password-store=basic")  # Use basic password storage to avoid keychain prompts
        
        driver = webdriver.Chrome(options=options)
        print("Chrome driver created successfully with TrueKey profile.")
        return driver
        
    except Exception as e:
        print(f"Failed to create Chrome driver with TrueKey profile: {e}")
        raise Exception("Failed to create Chrome driver. Please ensure Chrome is properly installed and try closing all Chrome processes.")

def find_truekey_extension_id():
    """
    Display instructions for finding the TrueKey extension ID manually.
    
    This helper function provides step-by-step instructions for users who need
    to locate their TrueKey extension ID in Chrome. It guides users through
    the Chrome extensions page and explains how to enable Developer mode to
    reveal extension IDs.
    
    The function displays:
    - How to navigate to Chrome extensions page
    - How to enable Developer mode
    - How to locate and copy the extension ID
    - Command line and environment variable usage examples
    
    Returns:
        None
        
    Note:
        This function is called when the --validate-only flag is used or
        when users need guidance on finding their extension ID.
        
    Example:
        The function will display output like:
        ```
        HOW TO FIND YOUR TRUEKEY EXTENSION ID:
        1. Open Chrome and go to: chrome://extensions/
        2. Enable 'Developer mode' (toggle in top-right corner)
        3. Find the TrueKey extension in the list
        4. Look for the extension ID (32-character string)
        5. Copy the extension ID and use it with the script
        ```
    """
    print("\n" + "="*60)
    print("HOW TO FIND YOUR TRUEKEY EXTENSION ID:")
    print("="*60)
    print("1. Open Chrome and go to: chrome://extensions/")
    print("2. Enable 'Developer mode' (toggle in top-right corner)")
    print("3. Find the TrueKey extension in the list")
    print("4. Look for the extension ID (32-character string)")
    print("5. Copy the extension ID and use it with the script:")
    print(f"   python3 delete-truekey-logins.py --extension-id YOUR_EXTENSION_ID")
    print("   OR set environment variable:")
    print(f"   export TRUEKEY_EXTENSION_ID=YOUR_EXTENSION_ID")
    print("="*60)

# --- Main Script Execution ---
# Validate extension ID if requested (validation mode)
if args.validate_only:
    print(f"Extension ID validation: {TRUEKEY_EXTENSION_ID}")
    find_truekey_extension_id()
    sys.exit(0)

# Create the Chrome WebDriver with TrueKey profile
driver = create_chrome_driver()
driver.get(TRUEKEY_DASHBOARD_URL)
time.sleep(3)  # Wait for page to load

# --- User Verification Step ---
# Pause for user to verify the TrueKey extension loaded properly
# This safety measure ensures the automation will work correctly
print("\n" + "="*60)
print("PAUSE: Please check if the TrueKey extension dashboard loaded properly.")
print("Look for the TrueKey interface in the browser window.")
print("="*60)
input("Press Enter to continue with the deletion process, or Ctrl+C to exit if the extension didn't load...")
print("Continuing with the deletion process...\n")

# --- Step 1: Switch to List View ---
# Click the list-mode icon to switch from grid view to list view
# This is necessary to make all login entries visible for deletion
try:
    list_mode_icon = driver.find_element(By.ID, "list-mode")
    list_mode_icon.click()
    time.sleep(2)  # Wait for the view to update
    print("Switched to list view successfully.")
except Exception as e:
    print("Couldn't click the list-mode icon. Error:", e)
    print("Continuing anyway - some entries might not be visible in grid view.")

# --- Step 2: Automated Deletion Process ---
# Systematically find and delete all login entries by clicking trash icons
# This loop continues until no more trash icons are found
print("Starting automated deletion process...")
deletion_count = 0

while True:
    # Find all trash icons with the specified SVG path
    # This XPath targets the specific trash icon used by TrueKey
    trash_icons = driver.find_elements(By.XPATH, '//img[contains(@src, "../images/common/svg/trash.svg")]')
    
    if not trash_icons:
        break  # No more trash icons visible; deletion complete
    
    print(f"Found {len(trash_icons)} items to delete...")
    
    # Process each trash icon found in the current view
    for icon in trash_icons:
        try:
            # Use ActionChains to ensure the icon is visible and clickable
            ActionChains(driver).move_to_element(icon).perform()
            icon.click()
            time.sleep(1)
            
            # Attempt to click confirmation dialog if it appears
            try:
                confirm_button = driver.find_element(By.XPATH, '//button[contains(text(), "Yes") or contains(text(), "Confirm")]')
                confirm_button.click()
                time.sleep(1)
                deletion_count += 1
                print(f"Deleted item #{deletion_count}")
            except Exception:
                # No confirmation dialog appeared, deletion was immediate
                deletion_count += 1
                print(f"Deleted item #{deletion_count}")
                
        except Exception as e:
            print(f"Skipping an icon due to error: {e}")
            continue

print(f"Completed deleting all items. Total deleted: {deletion_count}")

# --- Cleanup and Finalization ---
# Properly close the Chrome browser and display final information
try:
    driver.quit()
    print("Browser closed successfully.")
except Exception as e:
    print(f"Error during cleanup: {e}")

# Display profile management information for user reference
print(f"\nNote: TrueKey profile is saved at: /Users/[username]/Library/Application Support/Google/Chrome/TrueKey")
print("To refresh the profile with latest extensions, delete this directory and run the script again.")
