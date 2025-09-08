# Download Instructions for Bhaarat Browser

**Created by: Devesh Kumar**  
**Copyright © 2025 Devesh Kumar. All rights reserved.**

## 📥 How to Download the MSI Installer

The **BhaaratBrowser-1.0.1-win64.msi** installer (177 MB) is too large for GitHub's standard file hosting. Here are the available download options:

### Option 1: Build from Source (Recommended)
```bash
# Clone the repository
git clone https://github.com/DeveshKumarTR/MyWorkingBrowser01.git
cd MyWorkingBrowser01

# Install dependencies
py -m pip install PyQt6 PyQt6-WebEngine cx_Freeze

# Build the MSI installer
py setup.py bdist_msi
```

The installer will be created in the `dist/` folder as `BhaaratBrowser-1.0.1-win64.msi`.

### Option 2: Run Directly from Source
```bash
# Clone and run without building
git clone https://github.com/DeveshKumarTR/MyWorkingBrowser01.git
cd MyWorkingBrowser01

# Install dependencies
py -m pip install PyQt6 PyQt6-WebEngine

# Run the browser directly
py secure_browser.py
```

### Option 3: Download Portable Executable
After building from source, you can also find a portable executable at:
```
build/exe.win-amd64-3.11/BhaaratBrowser.exe
```

## 🔧 Build Requirements

- **Python 3.8+**
- **Windows 10/11** (64-bit)
- **Internet connection** (for downloading PyQt6 dependencies)
- **~500 MB free disk space** (for dependencies and build files)

## 📋 Build Process Details

1. **Clone Repository**: Downloads ~50 MB of source code
2. **Install Dependencies**: Downloads ~200 MB of PyQt6 components
3. **Build MSI**: Creates 177 MB professional installer
4. **Total Time**: 5-10 minutes depending on internet speed

## ✅ Verification

After building, verify the MSI installer:
- **File**: `dist/BhaaratBrowser-1.0.1-win64.msi`
- **Size**: ~177 MB
- **Creator**: Devesh Kumar
- **Version**: 1.0.1

## 🛠️ Alternative Distribution

For easier distribution, consider:
1. **Cloud Storage**: Upload MSI to Google Drive, OneDrive, or Dropbox
2. **File Hosting**: Use services like MediaFire or WeTransfer
3. **Local Network**: Share via local network or USB drives

## 📞 Support

If you encounter issues building the installer:
1. Ensure Python 3.8+ is installed
2. Verify internet connection for PyQt6 downloads
3. Check Windows version compatibility (Windows 10/11 required)
4. Contact: Repository issues at https://github.com/DeveshKumarTR/MyWorkingBrowser01/issues

---
**Bhaarat Browser v1.0.1 - Created by Devesh Kumar**
