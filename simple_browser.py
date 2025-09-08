#!/usr/bin/env python3
"""
Bhaarat Browser - Simple Version

Created by: Devesh Kumar
Copyright © 2025 Devesh Kumar. All rights reserved.

A minimal secure web browser application to test the core functionality.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class SimpleBrowser(QMainWindow):
    """Simple browser window for testing."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Bhaarat Browser - Simple by Devesh Kumar")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Navigation bar
        nav_layout = QHBoxLayout()
        
        # Back button
        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_btn)
        
        # Forward button
        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.go_forward)
        nav_layout.addWidget(self.forward_btn)
        
        # Reload button
        self.reload_btn = QPushButton("⟲")
        self.reload_btn.clicked.connect(self.reload_page)
        nav_layout.addWidget(self.reload_btn)
        
        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL...")
        self.address_bar.returnPressed.connect(self.navigate)
        nav_layout.addWidget(self.address_bar)
        
        # Go button
        go_btn = QPushButton("Go")
        go_btn.clicked.connect(self.navigate)
        nav_layout.addWidget(go_btn)
        
        layout.addLayout(nav_layout)
        
        # Web view
        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.update_address_bar)
        layout.addWidget(self.web_view)
        
        # Load home page
        self.web_view.setUrl(QUrl("https://www.google.com"))
        
    def navigate(self):
        """Navigate to the URL in the address bar."""
        url = self.address_bar.text().strip()
        if not url:
            return
            
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                # Treat as search query
                url = f'https://www.google.com/search?q={url}'
        
        self.web_view.setUrl(QUrl(url))
        
    def update_address_bar(self, url):
        """Update the address bar with the current URL."""
        self.address_bar.setText(url.toString())
        
    def go_back(self):
        """Navigate back."""
        self.web_view.back()
        
    def go_forward(self):
        """Navigate forward."""
        self.web_view.forward()
        
    def reload_page(self):
        """Reload the current page."""
        self.web_view.reload()


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Bhaarat Browser - Simple")
    
    browser = SimpleBrowser()
    browser.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
