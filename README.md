# Bhaarat Browser

[![Release](https://img.shields.io/github/v/release/DeveshKumarTR/MyWorkingBrowser01)](https://github.com/DeveshKumarTR/MyWorkingBrowser01/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/DeveshKumarTR/MyWorkingBrowser01)
[![Python](https://img.shields.io/badge/python-3.11+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

A secure, feature-rich web browser application built with Python and PyQt6, offering functionality similar to Internet Explorer and Chrome with modern security features and professional Windows distribution.

## Features

- **Tabbed Browsing**: Multiple tabs with easy navigation
- **Modern Web Engine**: Full HTML5, CSS3, and JavaScript support via QWebEngine
- **Security Indicators**: Visual indicators for secure (HTTPS) vs insecure (HTTP) connections
- **Bookmark Management**: Save and organize your favorite websites
- **Keyboard Shortcuts**: Full keyboard navigation support
- **Search Integration**: Smart address bar that handles both URLs and search queries
- **Zoom Controls**: Zoom in/out functionality
- **Multi-Window Support**: Open multiple browser windows
- **Find in Page**: Search within web pages

## 📥 Download

### For End Users (Recommended)
- **[Download Latest MSI Installer](https://github.com/DeveshKumarTR/MyWorkingBrowser01/releases/latest)** 
  - Professional Windows installer (177 MB)
  - No Python installation required
  - Creates desktop shortcuts and start menu entries
  - Automatic updates and uninstaller

### For Developers
- Clone this repository to build from source
- Portable executable available in releases

## Available Versions

1. **simple_browser.py** - Basic browser with essential functionality
2. **secure_browser.py** - Full-featured browser with all capabilities (recommended)
3. **main.py** - Advanced modular browser (under development)

## Requirements

- Python 3.8+
- PyQt6
- PyQt6-WebEngine

## Installation

1. Install dependencies:
```bash
py -m pip install PyQt6 PyQt6-WebEngine PyQt6-sip PyQt6-Qt6 PyQt6-WebEngine-Qt6 requests cryptography validators
```

2. Run the browser:
```bash
# Run the recommended secure browser
py secure_browser.py

# Or run the simple browser
py simple_browser.py
```

## Usage

### Basic Navigation
- **Address Bar**: Enter URLs or search terms
- **Navigation Buttons**: Back (←), Forward (→), Reload (⟲), Home (🏠)
- **Security Indicator**: 🔒 for secure HTTPS, ⚠️ for insecure HTTP

### Keyboard Shortcuts
- `Ctrl+T` - New tab
- `Ctrl+N` - New window
- `Ctrl+D` - Add bookmark
- `Ctrl+F` - Find in page
- `F5` - Reload page
- `Ctrl+=` - Zoom in
- `Ctrl+-` - Zoom out
- `Ctrl+Q` - Exit browser

### Tabs
- Click the `+` button to add new tabs
- Click the `×` button to close tabs
- Drag tabs to reorder them
- Right-click tabs for additional options

### Bookmarks
- Add bookmarks via `Ctrl+D` or the Bookmarks menu
- Quick access to bookmarks from the Bookmarks menu
- Bookmarks are automatically saved to your home directory

### Security Features
- HTTPS enforcement indicators
- Secure connection validation
- Safe browsing with modern web standards
- Automatic protocol detection (adds https:// when needed)

## Project Structure

```
Browser02/
├── secure_browser.py       # Main working browser (recommended)
├── simple_browser.py       # Basic browser version
├── main.py                 # Advanced modular browser (in development)
├── browser/                # Modular browser components
│   ├── browser_window.py   # Main browser window
│   ├── web_view.py         # Secure web view component
│   ├── tab_manager.py      # Tab management
│   ├── bookmark_manager.py # Bookmark functionality
│   ├── download_manager.py # Download handling
│   └── security/           # Security components
│       ├── ssl_handler.py  # SSL/TLS security
│       └── popup_blocker.py# Popup blocking
├── ui/                     # UI components
├── resources/              # Application resources
└── requirements.txt        # Python dependencies
```

## Development

The browser is built using:
- **PyQt6**: Modern Python GUI framework
- **QWebEngine**: Chromium-based web engine
- **Modular Architecture**: Separate components for different functionality

### Running from VS Code
Use the provided tasks:
- `Run Secure Browser` - Launch the full-featured browser
- `Run Simple Browser` - Launch the basic browser

## Security

This browser includes several security features:
- Secure connection indicators
- Modern web standards compliance
- Safe URL handling
- Protection against malicious content

## Known Issues

- Some advanced features in `main.py` are still under development
- Download manager requires additional integration
- Developer tools integration pending

## Contributing

This is a demonstration project showing how to build a modern web browser with Python and PyQt6. Feel free to extend and modify for your needs.

## License

This project is provided as-is for educational and demonstration purposes.
