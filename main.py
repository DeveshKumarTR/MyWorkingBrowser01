#!/usr/bin/env python3
"""
Bhaarat Browser - Main Application Entry Point

A secure web browser application with Internet Explorer and Chrome-like functionality.
Built with PyQt6 and QWebEngine for modern web standards support.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtWebEngineCore import QWebEngineProfile
from browser.browser_window import BrowserWindow


def setup_application():
    """Configure application settings and security policies."""
    # Create application first
    app = QApplication(sys.argv)
    app.setApplicationName("Bhaarat Browser")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("BhaaratBrowser")
    
    # Configure web engine security settings
    try:
        profile = QWebEngineProfile.defaultProfile()
        # Use basic profile configuration
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        profile.setHttpUserAgent(user_agent)
    except Exception as e:
        print(f"Warning: Could not configure web engine profile: {e}")
    
    return app


def main():
    """Main application entry point."""
    try:
        app = setup_application()
        
        # Create and show the main browser window
        browser = BrowserWindow()
        browser.show()
        
        # Load default homepage
        browser.load_homepage()
        
        # Start the application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting browser: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
