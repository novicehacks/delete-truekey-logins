# TrueKey Bulk Delete Script

This project provides a Python Selenium script to automate the deletion of all login entries in the TrueKey Chrome extension by switching the dashboard to list mode and then clicking the trash icons.

## Prerequisites

- **Python 3** installed on your Mac (recommend Python 3.8+)
- **Google Chrome** installed with the TrueKey extension and all logins already authenticated
- **Selenium** Python package installed
- **macOS** (script is optimized for macOS Chrome profile paths)

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

### 4. (Optional) Create a Python Virtual Environment
python3 -m venv venv
source venv/bin/activate

When done, you can deactivate with: deactivate
text

## How the Script Works

The script uses an intelligent profile management system:

1. **Automatic Profile Creation**: On first run, creates a dedicated "TrueKey" profile by copying your Chrome profile
2. **Profile Persistence**: Saves the TrueKey profile for reuse in subsequent runs (faster startup)
3. **Automatic Chrome Management**: Closes any running Chrome processes automatically
4. **Extension Preservation**: Copies your extensions (including TrueKey) to the dedicated profile

### Profile Location
The TrueKey profile is saved at:
```
/Users/[your-username]/Library/Application Support/Google/Chrome/TrueKey
```

### Refreshing the Profile
To update the profile with new extensions or settings:
```bash
rm -rf "/Users/[your-username]/Library/Application Support/Google/Chrome/TrueKey"
```
Then run the script again - it will recreate the profile from your current Chrome setup.

## Execution Instructions

1. **Ensure TrueKey is set up** in your main Chrome browser with all logins authenticated
2. Open a Terminal window
3. Change to your project/script directory
4. (Optional) Activate your Python virtual environment:
   ```bash
   source venv/bin/activate
   ```
5. Run the script:
   ```bash
   python3 delete-truekey-logins.py
   ```

### Extension ID Configuration

The script uses a default TrueKey extension ID (`cpaibbcbodhimfnjnakiidgbpiehfgci`), but you can configure it if needed:

> **📋 Need to find your extension ID?** See the [Finding Your Extension ID Guide](FINDING-EXTENSION-ID.md) for detailed instructions.

#### Option 1: Environment Variable
```bash
export TRUEKEY_EXTENSION_ID=your_extension_id_here
python3 delete-truekey-logins.py
```

#### Option 2: Command Line Argument
```bash
python3 delete-truekey-logins.py --extension-id your_extension_id_here
```

### Quick Extension ID Reference

For detailed instructions on finding your TrueKey extension ID, see the **[Finding Your Extension ID Guide](FINDING-EXTENSION-ID.md)**.

**Default TrueKey Extension ID:**
```
cpaibbcbodhimfnjnakiidgbpiehfgci
```

### What Happens During Execution

1. **Automatic Chrome Management**: Script automatically closes any running Chrome processes
2. **Profile Setup**: Creates or reuses the TrueKey profile (first run takes longer)
3. **Extension Loading**: Opens Chrome with the TrueKey extension dashboard
4. **User Verification**: Script pauses and asks you to verify the extension loaded properly
   - Press **Enter** to continue if the TrueKey dashboard is visible
   - Press **Ctrl+C** to exit if the extension didn't load
5. **Automated Deletion**: Switches to list view and deletes all login entries
6. **Cleanup**: Closes Chrome and displays completion message

## Notes and Troubleshooting

### Common Issues

- **"Chrome not reachable" error**: The script automatically handles this by creating a dedicated profile
- **Extension not loading**: Make sure TrueKey is properly installed and authenticated in your main Chrome browser
- **Profile conflicts**: The script uses a separate TrueKey profile to avoid conflicts with your main Chrome instance

### If You Encounter Issues

1. **Refresh the TrueKey profile**:
   ```bash
   rm -rf "/Users/[your-username]/Library/Application Support/Google/Chrome/TrueKey"
   ```

2. **Check Chrome installation**: Ensure Chrome is properly installed and updated

3. **Verify TrueKey extension**: Make sure the TrueKey extension is installed and working in your main Chrome browser

4. **Grant Accessibility Access**: If prompted, grant Terminal accessibility access in System Preferences > Security & Privacy > Privacy > Accessibility

### Important Warnings

- **BACK UP your TrueKey data** before running! This action is irreversible
- The script will pause for user verification - this is normal and important for safety
- You may need to update element selectors if the TrueKey UI changes in future versions

## Disclaimer

Use this script at your own risk. It will permanently delete all login entries in your TrueKey vault!

---