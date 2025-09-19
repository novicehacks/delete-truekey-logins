"""
TrueKey Login Deleter Script

IMPORTANT: Before running this script:
1. Close ALL Chrome browser windows and processes completely
2. Wait 2-3 seconds after closing Chrome
3. Then run this script

This ensures the Chrome profile isn't locked by another instance.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import tempfile

# --- Configuration ---
# Use your existing Chrome profile to access the TrueKey extension
import getpass
username = getpass.getuser()  # Gets current username dynamically
chrome_profile_path = f"/Users/{username}/Library/Application Support/Google/Chrome"

# TrueKey profile directory (permanent location for the copied profile)
truekey_profile_dir = f"/Users/{username}/Library/Application Support/Google/Chrome/TrueKey"

# Check if Chrome is running and attempt to close it
import subprocess
try:
    result = subprocess.run(['pgrep', '-f', 'Google Chrome'], capture_output=True, text=True)
    if result.stdout.strip():
        print("WARNING: Chrome appears to be running.")
        print("Attempting to close Chrome processes...")
        
        # Try to kill Chrome processes
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
    """Setup or update the TrueKey profile from the main Chrome profile"""
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
    """Create Chrome driver using the TrueKey profile"""
    
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
        options.add_argument(f"--user-data-dir={truekey_profile_dir}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=CrossSiteDocumentBlockingIfIsolating")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--disable-extensions-file-access-check")
        options.add_argument("--disable-extensions-http-throttling")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-field-trial-config")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        
        driver = webdriver.Chrome(options=options)
        print("Chrome driver created successfully with TrueKey profile.")
        return driver
        
    except Exception as e:
        print(f"Failed to create Chrome driver with TrueKey profile: {e}")
        raise Exception("Failed to create Chrome driver. Please ensure Chrome is properly installed and try closing all Chrome processes.")

# Create the driver
driver = create_chrome_driver()
driver.get("chrome-extension://cpaibbcbodhimfnjnakiidgbpiehfgci/html/dashboard.html")
time.sleep(3)  # Wait for page to load

# PAUSE: Check if the TrueKey extension is loaded
print("\n" + "="*60)
print("PAUSE: Please check if the TrueKey extension dashboard loaded properly.")
print("Look for the TrueKey interface in the browser window.")
print("="*60)
input("Press Enter to continue with the deletion process, or Ctrl+C to exit if the extension didn't load...")
print("Continuing with the deletion process...\n")

# --- Step 1: Click the "list-mode" image to switch to list view ---
try:
    list_mode_icon = driver.find_element(By.ID, "list-mode")
    list_mode_icon.click()
    time.sleep(2)  # Wait for the view to update
except Exception as e:
    print("Couldn't click the list-mode icon. Error:", e)

# --- Step 2: Find and delete all trash icons ---
while True:
    # Find all trash icons with the specified SVG path
    trash_icons = driver.find_elements(By.XPATH, '//img[contains(@src, "../images/common/svg/trash.svg")]')
    if not trash_icons:
        break  # No more trash icons visible; done

    for icon in trash_icons:
        try:
            ActionChains(driver).move_to_element(icon).perform()
            icon.click()
            time.sleep(1)
            # Attempt to click confirmation
            try:
                confirm_button = driver.find_element(By.XPATH, '//button[contains(text(), "Yes") or contains(text(), "Confirm")]')
                confirm_button.click()
                time.sleep(1)
            except Exception:
                pass
        except Exception as e:
            print("Skipping an icon due to error:", e)
            continue

print("Completed deleting all items shown with trash icons.")

# Clean up
try:
    driver.quit()
    print("Browser closed successfully.")
except Exception as e:
    print(f"Error during cleanup: {e}")

# Optional: Add a note about profile management
print(f"\nNote: TrueKey profile is saved at: /Users/[username]/Library/Application Support/Google/Chrome/TrueKey")
print("To refresh the profile with latest extensions, delete this directory and run the script again.")
