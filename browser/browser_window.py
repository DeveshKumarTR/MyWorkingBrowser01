"""
Browser Window - Main browser window with tabbed interface and navigation controls.

This module provides the main browser window that includes:
- Navigation toolbar with back, forward, refresh, home buttons
- Address bar with URL input and security indicators
- Tabbed browsing interface
- Menu bar with browser options
- Status bar for page loading information
"""

import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QTabWidget, QToolBar, QLineEdit, QPushButton, 
                             QMenuBar, QStatusBar, QMenu, QMessageBox, QInputDialog,
                             QFileDialog, QProgressBar, QLabel)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

from .web_view import SecureWebView
from .tab_manager import TabManager
from .bookmark_manager import BookmarkManager
from .download_manager import DownloadManager
from .security.ssl_handler import SSLHandler


class BrowserWindow(QMainWindow):
    """Main browser window with full browser functionality."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_managers()
        self.setup_security()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.setup_shortcuts()
        
    def init_ui(self):
        """Initialize the main user interface."""
        self.setWindowTitle("Bhaarat Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create tab widget for multiple tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        layout.addWidget(self.tab_widget)
        
        # Add initial tab
        self.add_new_tab("https://www.google.com")
        
    def setup_managers(self):
        """Initialize browser managers."""
        try:
            self.tab_manager = TabManager(self.tab_widget)
            self.bookmark_manager = BookmarkManager()
            self.download_manager = DownloadManager()
        except Exception as e:
            print(f"Warning: Could not initialize all managers: {e}")
            # Initialize basic managers
            from .tab_manager import TabManager
            self.tab_manager = TabManager(self.tab_widget)
        
    def setup_security(self):
        """Initialize security components."""
        self.ssl_handler = SSLHandler()
        
    def create_menus(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_tab_action = QAction('New Tab', self)
        new_tab_action.setShortcut(QKeySequence.StandardKey.AddTab)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)
        
        new_window_action = QAction('New Window', self)
        new_window_action.setShortcut(QKeySequence.StandardKey.New)
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)
        
        new_incognito_action = QAction('New Incognito Window', self)
        new_incognito_action.setShortcut(QKeySequence('Ctrl+Shift+N'))
        new_incognito_action.triggered.connect(self.new_incognito_window)
        file_menu.addAction(new_incognito_action)
        
        file_menu.addSeparator()
        
        save_page_action = QAction('Save Page As...', self)
        save_page_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_page_action.triggered.connect(self.save_page)
        file_menu.addAction(save_page_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        find_action = QAction('Find', self)
        find_action.setShortcut(QKeySequence.StandardKey.Find)
        find_action.triggered.connect(self.find_in_page)
        edit_menu.addAction(find_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        reload_action = QAction('Reload', self)
        reload_action.setShortcut(QKeySequence.StandardKey.Refresh)
        reload_action.triggered.connect(self.reload_page)
        view_menu.addAction(reload_action)
        
        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        # Bookmarks menu
        bookmarks_menu = menubar.addMenu('Bookmarks')
        
        add_bookmark_action = QAction('Add Bookmark', self)
        add_bookmark_action.setShortcut(QKeySequence('Ctrl+D'))
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)
        
        show_bookmarks_action = QAction('Show All Bookmarks', self)
        show_bookmarks_action.triggered.connect(self.show_bookmarks)
        bookmarks_menu.addAction(show_bookmarks_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        downloads_action = QAction('Downloads', self)
        downloads_action.setShortcut(QKeySequence('Ctrl+Shift+J'))
        downloads_action.triggered.connect(self.show_downloads)
        tools_menu.addAction(downloads_action)
        
        developer_tools_action = QAction('Developer Tools', self)
        developer_tools_action.setShortcut(QKeySequence('F12'))
        developer_tools_action.triggered.connect(self.show_developer_tools)
        tools_menu.addAction(developer_tools_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Create the navigation toolbar."""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Navigation buttons
        self.back_btn = QPushButton('←')
        self.back_btn.setToolTip('Go back')
        self.back_btn.clicked.connect(self.go_back)
        toolbar.addWidget(self.back_btn)
        
        self.forward_btn = QPushButton('→')
        self.forward_btn.setToolTip('Go forward')
        self.forward_btn.clicked.connect(self.go_forward)
        toolbar.addWidget(self.forward_btn)
        
        self.reload_btn = QPushButton('⟲')
        self.reload_btn.setToolTip('Reload page')
        self.reload_btn.clicked.connect(self.reload_page)
        toolbar.addWidget(self.reload_btn)
        
        self.home_btn = QPushButton('🏠')
        self.home_btn.setToolTip('Go home')
        self.home_btn.clicked.connect(self.go_home)
        toolbar.addWidget(self.home_btn)
        
        # Address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText('Enter URL or search term...')
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.address_bar)
        
        # Security indicator
        self.security_label = QLabel('🔒')
        self.security_label.setToolTip('Connection security')
        toolbar.addWidget(self.security_label)
        
        # Menu button
        menu_btn = QPushButton('☰')
        menu_btn.setToolTip('Menu')
        menu_btn.clicked.connect(self.show_menu)
        toolbar.addWidget(menu_btn)
        
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Progress bar for page loading
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Tab shortcuts
        for i in range(1, 10):
            shortcut = QKeySequence(f'Ctrl+{i}')
            action = QAction(self)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda checked, tab=i-1: self.switch_to_tab(tab))
            self.addAction(action)
    
    def add_new_tab(self, url="https://www.google.com", label="New Tab"):
        """Add a new tab with the specified URL."""
        web_view = SecureWebView()
        web_view.urlChanged.connect(self.update_address_bar)
        web_view.titleChanged.connect(self.update_tab_title)
        web_view.loadStarted.connect(self.load_started)
        web_view.loadProgress.connect(self.load_progress)
        web_view.loadFinished.connect(self.load_finished)
        
        # Setup download handling
        try:
            web_view.page().profile().downloadRequested.connect(
                self.download_manager.download_requested
            )
        except Exception as e:
            print(f"Warning: Could not setup download handling: {e}")
        
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
    
    def update_address_bar(self, url):
        """Update the address bar with the current URL."""
        self.address_bar.setText(url.toString())
        self.update_security_indicator(url)
    
    def update_security_indicator(self, url):
        """Update the security indicator based on the URL scheme."""
        if url.scheme() == 'https':
            self.security_label.setText('🔒')
            self.security_label.setToolTip('Secure connection')
        else:
            self.security_label.setText('⚠️')
            self.security_label.setToolTip('Insecure connection')
    
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
        self.back_btn.setEnabled(web_view.history().canGoBack())
        self.forward_btn.setEnabled(web_view.history().canGoForward())
    
    def load_started(self):
        """Handle page load start."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_bar.showMessage("Loading...")
    
    def load_progress(self, progress):
        """Handle page load progress."""
        self.progress_bar.setValue(progress)
    
    def load_finished(self, success):
        """Handle page load completion."""
        self.progress_bar.setVisible(False)
        if success:
            self.status_bar.showMessage("Ready", 2000)
        else:
            self.status_bar.showMessage("Failed to load page", 2000)
        
        # Update navigation buttons
        web_view = self.current_web_view()
        if web_view:
            self.update_navigation_buttons(web_view)
    
    def load_homepage(self):
        """Load the homepage in the current tab."""
        web_view = self.current_web_view()
        if web_view:
            web_view.setUrl(QUrl("https://www.google.com"))
    
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
        self.load_homepage()
    
    # Tab management methods
    def new_tab(self):
        """Create a new tab."""
        self.add_new_tab()
    
    def new_window(self):
        """Open a new browser window."""
        new_window = BrowserWindow()
        new_window.show()
    
    def new_incognito_window(self):
        """Open a new incognito window."""
        new_window = BrowserWindow()
        new_window.setWindowTitle("Bhaarat Browser (Incognito)")
        new_window.show()
    
    def switch_to_tab(self, index):
        """Switch to the specified tab index."""
        if 0 <= index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(index)
    
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
    
    # File methods
    def save_page(self):
        """Save the current page."""
        web_view = self.current_web_view()
        if web_view:
            filename, _ = QFileDialog.getSaveFileName(
                self, 'Save Page', 'page.html', 'HTML files (*.html)'
            )
            if filename:
                # Note: Actual page saving would require additional implementation
                QMessageBox.information(self, 'Save Page', 'Page saving functionality would be implemented here.')
    
    # Bookmark methods
    def add_bookmark(self):
        """Add current page to bookmarks."""
        web_view = self.current_web_view()
        if web_view:
            url = web_view.url().toString()
            title = web_view.title()
            self.bookmark_manager.add_bookmark(title, url)
            QMessageBox.information(self, 'Bookmark Added', f'Added bookmark: {title}')
    
    def show_bookmarks(self):
        """Show bookmarks manager."""
        self.bookmark_manager.show_bookmarks_dialog(self)
    
    # Tools methods
    def show_downloads(self):
        """Show downloads manager."""
        self.download_manager.show_downloads_dialog(self)
    
    def show_developer_tools(self):
        """Show developer tools."""
        web_view = self.current_web_view()
        if web_view:
            # Note: Developer tools integration would require additional implementation
            QMessageBox.information(self, 'Developer Tools', 'Developer tools would be opened here.')
    
    def show_menu(self):
        """Show application menu."""
        # This could show a context menu or additional options
        pass
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, 'About Bhaarat Browser', 
                         'Bhaarat Browser v1.0.0\n\n'
                         'A secure web browser with modern functionality.\n'
                         'Built with PyQt6 and QWebEngine.')
    
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
