"""
Bookmark Manager - Handle bookmark storage and management.

This module provides functionality for managing bookmarks including
adding, removing, organizing, and importing/exporting bookmarks.
"""

import json
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QListWidgetItem, QPushButton, QLineEdit, QLabel,
                             QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QUrl


class BookmarkManager:
    """Manages browser bookmarks."""
    
    def __init__(self):
        self.bookmarks_file = os.path.join(os.path.expanduser("~"), ".secure_browser_bookmarks.json")
        self.bookmarks = self.load_bookmarks()
        
    def load_bookmarks(self):
        """Load bookmarks from file."""
        try:
            if os.path.exists(self.bookmarks_file):
                with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
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
        try:
            with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving bookmarks: {e}")
            return False
            
    def add_bookmark(self, title, url):
        """Add a new bookmark."""
        bookmark = {
            "title": title or url,
            "url": url
        }
        
        # Check if bookmark already exists
        for existing in self.bookmarks:
            if existing["url"] == url:
                existing["title"] = title  # Update title if URL exists
                self.save_bookmarks()
                return False  # Indicate it was an update, not addition
                
        self.bookmarks.append(bookmark)
        self.save_bookmarks()
        return True
        
    def remove_bookmark(self, url):
        """Remove a bookmark by URL."""
        self.bookmarks = [b for b in self.bookmarks if b["url"] != url]
        self.save_bookmarks()
        
    def get_bookmarks(self):
        """Get all bookmarks."""
        return self.bookmarks.copy()
        
    def search_bookmarks(self, query):
        """Search bookmarks by title or URL."""
        query = query.lower()
        return [b for b in self.bookmarks 
                if query in b["title"].lower() or query in b["url"].lower()]
                
    def show_bookmarks_dialog(self, parent):
        """Show bookmarks management dialog."""
        dialog = BookmarksDialog(self, parent)
        dialog.exec()


class BookmarksDialog(QDialog):
    """Dialog for managing bookmarks."""
    
    def __init__(self, bookmark_manager, parent=None):
        super().__init__(parent)
        self.bookmark_manager = bookmark_manager
        self.init_ui()
        self.load_bookmarks_list()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Bookmarks Manager")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_bookmarks)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Bookmarks list
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(self.bookmarks_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Bookmark")
        add_btn.clicked.connect(self.add_bookmark)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_bookmark)
        button_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_bookmark)
        button_layout.addWidget(remove_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def load_bookmarks_list(self):
        """Load bookmarks into the list widget."""
        self.bookmarks_list.clear()
        for bookmark in self.bookmark_manager.get_bookmarks():
            item = QListWidgetItem(f"{bookmark['title']} - {bookmark['url']}")
            item.setData(Qt.ItemDataRole.UserRole, bookmark)
            self.bookmarks_list.addItem(item)
            
    def filter_bookmarks(self, query):
        """Filter bookmarks based on search query."""
        if not query:
            self.load_bookmarks_list()
            return
            
        self.bookmarks_list.clear()
        filtered = self.bookmark_manager.search_bookmarks(query)
        for bookmark in filtered:
            item = QListWidgetItem(f"{bookmark['title']} - {bookmark['url']}")
            item.setData(Qt.ItemDataRole.UserRole, bookmark)
            self.bookmarks_list.addItem(item)
            
    def add_bookmark(self):
        """Add a new bookmark."""
        title, ok1 = QInputDialog.getText(self, "Add Bookmark", "Title:")
        if ok1 and title:
            url, ok2 = QInputDialog.getText(self, "Add Bookmark", "URL:")
            if ok2 and url:
                self.bookmark_manager.add_bookmark(title, url)
                self.load_bookmarks_list()
                
    def edit_bookmark(self):
        """Edit the selected bookmark."""
        current_item = self.bookmarks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a bookmark to edit.")
            return
            
        bookmark = current_item.data(Qt.ItemDataRole.UserRole)
        
        title, ok1 = QInputDialog.getText(self, "Edit Bookmark", "Title:", text=bookmark['title'])
        if ok1:
            url, ok2 = QInputDialog.getText(self, "Edit Bookmark", "URL:", text=bookmark['url'])
            if ok2:
                # Remove old bookmark
                self.bookmark_manager.remove_bookmark(bookmark['url'])
                # Add updated bookmark
                self.bookmark_manager.add_bookmark(title, url)
                self.load_bookmarks_list()
                
    def remove_bookmark(self):
        """Remove the selected bookmark."""
        current_item = self.bookmarks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a bookmark to remove.")
            return
            
        bookmark = current_item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(self, "Remove Bookmark", 
                                   f"Remove bookmark '{bookmark['title']}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.bookmark_manager.remove_bookmark(bookmark['url'])
            self.load_bookmarks_list()
            
    def open_bookmark(self, item):
        """Open the selected bookmark."""
        bookmark = item.data(Qt.ItemDataRole.UserRole)
        if self.parent():
            # Try to open in parent browser window
            web_view = self.parent().current_web_view()
            if web_view:
                web_view.setUrl(QUrl(bookmark['url']))
                self.close()
