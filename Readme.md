# True Key Bulk Delete Script

This project provides a Python Selenium script to automate the deletion of all login entries in the True Key Chrome extension by switching the dashboard to list mode and then clicking the trash icons.

## Prerequisites

- **Python 3** installed on your Mac (recommend Python 3.8+)
- **Google Chrome** installed with the True Key extension and all logins already authenticated
- **ChromeDriver** installed (matching your Chrome version)
- **Selenium** Python package installed

## Setup Instructions

### 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

text

### 2. Install Python 3 (if not installed)
brew install python

text

### 3. Install Selenium
pip3 install selenium

text

### 4. Download and Install ChromeDriver
- Check your Chrome version via `chrome://settings/help`.
- Download the matching ChromeDriver from [chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
- Move ChromeDriver to your PATH (e.g., `/usr/local/bin`):
mv ~/Downloads/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

text

### 5. Find Your Chrome Profile Path
- Open Chrome and go to `chrome://version/`.
- Find and note your "Profile Path" (e.g., `/Users/youruser/Library/Application Support/Google/Chrome`).

### 6. (Optional) Create a Python Virtual Environment
python3 -m venv venv
source venv/bin/activate

When done, you can deactivate with: deactivate
text

## Script Configuration

- Download or copy the script to a file, e.g., `delete_truekey_logins.py`.
- **Edit the script**: Set the `chrome_profile_path` variable to match your Chrome profile path found above.  
  Example:  
chrome_profile_path = "/Users/youruser/Library/Application Support/Google/Chrome"

text
- By default, the script uses the "Default" profile directory. Edit if you use another profile.

## Execution Instructions

1. Open a Terminal window.
2. Change to your project/script directory.
3. (Optional) Activate your Python virtual environment:
source venv/bin/activate

text
4. Run the script:
python3 delete_truekey_logins.py

text

## Notes and Troubleshooting

- **Selenium can’t always automate Chrome extension UIs** due to security restrictions. This script works best when the extension is unlocked and active in your Chrome profile.
- If Chrome shows `ERR_BLOCKED_BY_CLIENT` or a blank page, try:
 - Ensuring you’re running Selenium with your real user profile
 - Adding flags like `--disable-web-security` as shown in the script
 - Granting Accessibility Access to Terminal (System Preferences > Security & Privacy > Privacy > Accessibility)
- BACK UP your True Key data before running! This action is irreversible.
- You may need to update element selectors if the True Key UI changes in future versions.

## Disclaimer

Use this script at your own risk. It will permanently delete all login entries in your True Key vault!

---