#!/usr/bin/env python3
"""
Bhaarat Browser - Secure Web Browser

Created by: Devesh Kumar
Copyright © 2025 Devesh Kumar. All rights reserved.

A secure web browser application with essential functionality.
Modern web browsing with security features and professional interface.
"""

import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLineEdit, QTabWidget, QMenuBar,
                             QStatusBar, QMessageBox, QInputDialog)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QAction, QKeySequence


class SecureBrowser(QMainWindow):
    """Main secure browser window."""
    
    def __init__(self):
        super().__init__()
        self.bookmarks = self.load_bookmarks()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Bhaarat Browser - by Devesh Kumar")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create menus
        self.create_menus()
        
        # Navigation toolbar
        nav_layout = QHBoxLayout()
        
        # Navigation buttons
        self.back_btn = QPushButton("←")
        self.back_btn.setToolTip("Go back")
        self.back_btn.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton("→")
        self.forward_btn.setToolTip("Go forward")
        self.forward_btn.clicked.connect(self.go_forward)
        nav_layout.addWidget(self.forward_btn)
        
        self.reload_btn = QPushButton("⟲")
        self.reload_btn.setToolTip("Reload page")
        self.reload_btn.clicked.connect(self.reload_page)
        nav_layout.addWidget(self.reload_btn)
        
        self.home_btn = QPushButton("🏠")
        self.home_btn.setToolTip("Go home")
        self.home_btn.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_btn)
        
        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL or search term...")
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        nav_layout.addWidget(self.address_bar)
        
        # Security indicator
        self.security_label = QPushButton("🔒")
        self.security_label.setToolTip("Connection security")
        self.security_label.setMaximumWidth(40)
        nav_layout.addWidget(self.security_label)
        
        layout.addLayout(nav_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        layout.addWidget(self.tab_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add initial tab
        self.add_new_tab("https://www.google.com")
        
    def create_menus(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_tab_action = QAction('New Tab', self)
        new_tab_action.setShortcut(QKeySequence('Ctrl+T'))
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction('New Window', self)
        new_window_action.setShortcut(QKeySequence('Ctrl+N'))
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        find_action = QAction('Find', self)
        find_action.setShortcut(QKeySequence('Ctrl+F'))
        find_action.triggered.connect(self.find_in_page)
        edit_menu.addAction(find_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        reload_action = QAction('Reload', self)
        reload_action.setShortcut(QKeySequence('F5'))
        reload_action.triggered.connect(self.reload_page)
        view_menu.addAction(reload_action)
        
        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.setShortcut(QKeySequence('Ctrl+='))
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.setShortcut(QKeySequence('Ctrl+-'))
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        # Bookmarks menu
        bookmarks_menu = menubar.addMenu('Bookmarks')
        
        add_bookmark_action = QAction('Add Bookmark', self)
        add_bookmark_action.setShortcut(QKeySequence('Ctrl+D'))
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)
        
        bookmarks_menu.addSeparator()
        
        # Add bookmark shortcuts
        for bookmark in self.bookmarks[:10]:  # Limit to 10 bookmarks in menu
            action = QAction(bookmark['title'], self)
            action.triggered.connect(lambda checked, url=bookmark['url']: self.navigate_to_bookmark(url))
            bookmarks_menu.addAction(action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def add_new_tab(self, url="https://www.google.com", label="New Tab"):
        """Add a new tab with the specified URL."""
        web_view = QWebEngineView()
        web_view.urlChanged.connect(self.update_address_bar)
        web_view.titleChanged.connect(self.update_tab_title)
        web_view.loadStarted.connect(self.load_started)
        web_view.loadFinished.connect(self.load_finished)
        
        index = self.tab_widget.addTab(web_view, label)
        self.tab_widget.setCurrentIndex(index)
        
        if url:
            web_view.setUrl(QUrl(url))
            
        return web_view
    
    def close_tab(self, index):
        """Close the tab at the specified index."""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()
    
    def tab_changed(self, index):
        """Handle tab change events."""
        if index >= 0:
            web_view = self.tab_widget.widget(index)
            if web_view:
                self.update_address_bar(web_view.url())
                self.update_navigation_buttons(web_view)
    
    def current_web_view(self):
        """Get the current active web view."""
        return self.tab_widget.currentWidget()
    
    def navigate_to_url(self):
        """Navigate to the URL in the address bar."""
        url = self.address_bar.text().strip()
        if not url:
            return
            
        # Add protocol if missing
        if not url.startswith(('http://', 'https://', 'file://')):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                # Treat as search query
                url = f'https://www.google.com/search?q={url}'
        
        web_view = self.current_web_view()
        if web_view:
            web_view.setUrl(QUrl(url))
    
    def navigate_to_bookmark(self, url):
        """Navigate to a bookmark URL."""
        web_view = self.current_web_view()
        if web_view:
            web_view.setUrl(QUrl(url))
    
    def update_address_bar(self, url):
        """Update the address bar with the current URL."""
        self.address_bar.setText(url.toString())
        self.update_security_indicator(url)
    
    def update_security_indicator(self, url):
        """Update the security indicator based on the URL scheme."""
        if url.scheme() == 'https':
            self.security_label.setText('🔒')
            self.security_label.setToolTip('Secure connection')
            self.security_label.setStyleSheet("QPushButton { color: green; }")
        else:
            self.security_label.setText('⚠️')
            self.security_label.setToolTip('Insecure connection')
            self.security_label.setStyleSheet("QPushButton { color: orange; }")
    
    def update_tab_title(self, title):
        """Update the current tab title."""
        index = self.tab_widget.currentIndex()
        if index >= 0:
            # Limit title length
            if len(title) > 20:
                title = title[:17] + "..."
            self.tab_widget.setTabText(index, title or "Loading...")
    
    def update_navigation_buttons(self, web_view):
        """Update navigation button states."""
        if hasattr(web_view, 'history'):
            self.back_btn.setEnabled(web_view.history().canGoBack())
            self.forward_btn.setEnabled(web_view.history().canGoForward())
    
    def load_started(self):
        """Handle page load start."""
        self.status_bar.showMessage("Loading...")
    
    def load_finished(self, success):
        """Handle page load completion."""
        if success:
            self.status_bar.showMessage("Ready", 2000)
        else:
            self.status_bar.showMessage("Failed to load page", 2000)
        
        # Update navigation buttons
        web_view = self.current_web_view()
        if web_view:
            self.update_navigation_buttons(web_view)
    
    # Navigation methods
    def go_back(self):
        """Navigate back in history."""
        web_view = self.current_web_view()
        if web_view:
            web_view.back()
    
    def go_forward(self):
        """Navigate forward in history."""
        web_view = self.current_web_view()
        if web_view:
            web_view.forward()
    
    def reload_page(self):
        """Reload the current page."""
        web_view = self.current_web_view()
        if web_view:
            web_view.reload()
    
    def go_home(self):
        """Navigate to the home page."""
        web_view = self.current_web_view()
        if web_view:
            web_view.setUrl(QUrl("https://www.google.com"))
    
    # Tab management methods
    def new_tab(self):
        """Create a new tab."""
        self.add_new_tab()
    
    def new_window(self):
        """Open a new browser window."""
        new_window = SecureBrowser()
        new_window.show()
    
    # View methods
    def zoom_in(self):
        """Zoom in the current page."""
        web_view = self.current_web_view()
        if web_view:
            current_zoom = web_view.zoomFactor()
            web_view.setZoomFactor(min(current_zoom * 1.1, 3.0))
    
    def zoom_out(self):
        """Zoom out the current page."""
        web_view = self.current_web_view()
        if web_view:
            current_zoom = web_view.zoomFactor()
            web_view.setZoomFactor(max(current_zoom * 0.9, 0.25))
    
    def find_in_page(self):
        """Open find dialog for the current page."""
        text, ok = QInputDialog.getText(self, 'Find in Page', 'Enter text to find:')
        if ok and text:
            web_view = self.current_web_view()
            if web_view:
                web_view.findText(text)
    
    # Bookmark methods
    def load_bookmarks(self):
        """Load bookmarks from file."""
        bookmarks_file = os.path.join(os.path.expanduser("~"), ".secure_browser_bookmarks.json")
        try:
            if os.path.exists(bookmarks_file):
                with open(bookmarks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading bookmarks: {e}")
        
        # Return default bookmarks if file doesn't exist or is corrupted
        return [
            {"title": "Google", "url": "https://www.google.com"},
            {"title": "GitHub", "url": "https://github.com"},
            {"title": "Stack Overflow", "url": "https://stackoverflow.com"},
        ]
    
    def save_bookmarks(self):
        """Save bookmarks to file."""
        bookmarks_file = os.path.join(os.path.expanduser("~"), ".secure_browser_bookmarks.json")
        try:
            with open(bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving bookmarks: {e}")
            return False
    
    def add_bookmark(self):
        """Add current page to bookmarks."""
        web_view = self.current_web_view()
        if web_view:
            url = web_view.url().toString()
            title = web_view.title() or url
            
            # Check if bookmark already exists
            for bookmark in self.bookmarks:
                if bookmark["url"] == url:
                    QMessageBox.information(self, 'Bookmark', 'Bookmark already exists!')
                    return
            
            bookmark = {"title": title, "url": url}
            self.bookmarks.append(bookmark)
            self.save_bookmarks()
            QMessageBox.information(self, 'Bookmark Added', f'Added bookmark: {title}')
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, 'About Bhaarat Browser', 
                         'Bhaarat Browser v1.0.0\n\n'
                         'A secure web browser with modern functionality.\n'
                         'Built with PyQt6 and QWebEngine.\n\n'
                         'Features:\n'
                         '• Tabbed browsing\n'
                         '• Bookmark management\n'
                         '• Security indicators\n'
                         '• Modern web engine\n'
                         '• Keyboard shortcuts')
    
    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(self, 'Close Bhaarat Browser', 
                                   'Are you sure you want to close the browser?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """Main application entry point."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Bhaarat Browser")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("BhaaratBrowser")
        
        browser = SecureBrowser()
        browser.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting browser: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
