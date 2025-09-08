"""
Tab Manager - Handle tab operations and management.

This module provides functionality for managing browser tabs including
creation, deletion, reordering, and tab state management.
"""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtCore import QObject, pyqtSignal


class TabManager(QObject):
    """Manages browser tabs and their operations."""
    
    tab_added = pyqtSignal(int)  # Tab index
    tab_removed = pyqtSignal(int)  # Tab index
    tab_changed = pyqtSignal(int)  # Tab index
    
    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget
        self.setup_connections()
        
    def setup_connections(self):
        """Setup signal connections."""
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.tabCloseRequested.connect(self.on_tab_close_requested)
        
    def add_tab(self, widget, title="New Tab"):
        """Add a new tab with the given widget."""
        index = self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentIndex(index)
        self.tab_added.emit(index)
        return index
        
    def remove_tab(self, index):
        """Remove tab at the specified index."""
        if self.tab_widget.count() > 1:
            widget = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            if widget:
                widget.deleteLater()
            self.tab_removed.emit(index)
            return True
        return False
        
    def get_current_tab(self):
        """Get the current active tab widget."""
        return self.tab_widget.currentWidget()
        
    def get_current_index(self):
        """Get the current active tab index."""
        return self.tab_widget.currentIndex()
        
    def set_current_tab(self, index):
        """Set the active tab by index."""
        if 0 <= index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(index)
            
    def get_tab_count(self):
        """Get the total number of tabs."""
        return self.tab_widget.count()
        
    def update_tab_title(self, index, title):
        """Update the title of the tab at the specified index."""
        if 0 <= index < self.tab_widget.count():
            # Limit title length for display
            if len(title) > 20:
                title = title[:17] + "..."
            self.tab_widget.setTabText(index, title)
            
    def on_tab_changed(self, index):
        """Handle tab change events."""
        self.tab_changed.emit(index)
        
    def on_tab_close_requested(self, index):
        """Handle tab close requests."""
        self.remove_tab(index)
        
    def close_all_tabs_except(self, keep_index):
        """Close all tabs except the specified one."""
        indices_to_remove = []
        for i in range(self.tab_widget.count()):
            if i != keep_index:
                indices_to_remove.append(i)
                
        # Remove in reverse order to maintain correct indices
        for i in reversed(indices_to_remove):
            self.remove_tab(i)
            
    def duplicate_tab(self, index):
        """Duplicate the tab at the specified index."""
        widget = self.tab_widget.widget(index)
        if widget and hasattr(widget, 'url'):
            # Create new tab with same URL
            from .web_view import SecureWebView
            new_web_view = SecureWebView()
            new_web_view.setUrl(widget.url())
            title = self.tab_widget.tabText(index)
            return self.add_tab(new_web_view, f"{title} (Copy)")
        return -1
