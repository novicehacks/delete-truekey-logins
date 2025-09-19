# Finding Your Extension ID

If you need to find your TrueKey extension ID, you have several options:

## Method 1: Using the Script's Validation Tool

The easiest way to get instructions:

```bash
python3 delete-truekey-logins.py --validate-only
```

This will display step-by-step instructions and show you the current extension ID being used.

## Method 2: Manual Discovery via Chrome Extensions Page

Follow these detailed steps to find your TrueKey extension ID:

### Step 1: Open Chrome Extensions Page
1. Open Google Chrome
2. Navigate to: `chrome://extensions/`
   - **Alternative**: Click the three-dot menu → More tools → Extensions

### Step 2: Enable Developer Mode
1. Look for the **"Developer mode"** toggle in the top-right corner
2. Click the toggle to enable it (it should turn blue/active)
3. This reveals additional information about your extensions

### Step 3: Locate TrueKey Extension
1. Scroll through the list of extensions to find **TrueKey**
2. Look for the TrueKey icon and name in the extension list
3. If you don't see it, make sure it's installed and enabled

### Step 4: Find the Extension ID
1. With Developer mode enabled, you'll see additional details for each extension
2. Look for the **"ID"** field under the TrueKey extension
3. The ID will be a **32-character alphanumeric string** (e.g., `cpaibbcbodhimfnjnakiidgbpiehfgci`)
4. Copy this ID - you'll need it for the script

### Step 5: Verify the Extension ID Format
- ✅ **Correct format**: 32 characters, lowercase letters and numbers only
- ❌ **Incorrect format**: Contains uppercase letters, special characters, or wrong length

## Method 3: Using Chrome Developer Tools

For advanced users, you can also find the extension ID using Chrome's developer tools:

1. Open Chrome and go to any webpage
2. Press `F12` or right-click → "Inspect"
3. In the Console tab, type: `chrome.runtime.id`
4. Press Enter - this will show the extension ID if you're on an extension page

## Troubleshooting Extension ID Issues

### TrueKey Extension Not Found
- **Check installation**: Ensure TrueKey is properly installed from the Chrome Web Store
- **Check enablement**: Make sure the extension is enabled (toggle should be blue)
- **Check updates**: Update the extension to the latest version

### Extension ID Format Issues
- **Wrong length**: Extension IDs are exactly 32 characters
- **Wrong characters**: Only lowercase letters (a-z) and numbers (0-9) are allowed
- **Case sensitivity**: Extension IDs are case-sensitive

### Multiple TrueKey Extensions
If you have multiple TrueKey-related extensions:
- Look for the main **TrueKey** extension (not helper extensions)
- Check the extension description to confirm it's the correct one
- The main TrueKey extension typically has the standard ID: `cpaibbcbodhimfnjnakiidgbpiehfgci`

## Extension ID Format Example

Extension IDs are 32-character alphanumeric strings. Here's an example:

**Default TrueKey Extension ID:**
```
cpaibbcbodhimfnjnakiidgbpiehfgci
```

**Example Usage:**
```bash
# Using the default extension ID
python3 delete-truekey-logins.py

# Using a custom extension ID
python3 delete-truekey-logins.py --extension-id cpaibbcbodhimfnjnakiidgbpiehfgci

# Using environment variable
export TRUEKEY_EXTENSION_ID=cpaibbcbodhimfnjnakiidgbpiehfgci
python3 delete-truekey-logins.py
```

**Note:** The extension ID should be exactly 32 characters long and contain only lowercase letters and numbers.

## References

- **Chrome Extensions Developer Guide**: [Chrome Developer Documentation](https://developer.chrome.com/docs/extensions/)
- **Extension ID Information**: [Chrome Extensions Architecture](https://developer.chrome.com/docs/extensions/mv3/architecture-overview/#extension-id)
- **Chrome Extensions Page**: Access via `chrome://extensions/` in your browser
