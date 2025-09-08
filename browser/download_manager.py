"""
Download Manager - Handle file downloads and management.

This module provides functionality for managing downloads including
download progress tracking, file management, and download history.
"""

import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QLabel, QProgressBar,
                             QMessageBox, QFileDialog, QWidget)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QTimer, QUrl
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest


class DownloadItem(QObject):
    """Represents a single download item."""
    
    progress_updated = pyqtSignal(int)  # Progress percentage
    download_finished = pyqtSignal(bool)  # Success status
    
    def __init__(self, download_request):
        super().__init__()
        self.download_request = download_request
        self.file_path = ""
        self.file_name = ""
        self.total_bytes = 0
        self.received_bytes = 0
        self.state = "pending"
        self.start_time = datetime.now()
        
        self.setup_download()
        
    def setup_download(self):
        """Setup the download request."""
        self.file_name = self.download_request.suggestedFileName()
        if not self.file_name:
            self.file_name = "download"
            
        # Set default download directory
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
            
        self.file_path = os.path.join(downloads_dir, self.file_name)
        self.download_request.setDownloadDirectory(downloads_dir)
        self.download_request.setDownloadFileName(self.file_name)
        
        # Connect signals
        self.download_request.downloadProgress.connect(self.on_progress)
        self.download_request.finished.connect(self.on_finished)
        
    def start_download(self):
        """Start the download."""
        self.download_request.accept()
        self.state = "downloading"
        
    def on_progress(self, received, total):
        """Handle download progress updates."""
        self.received_bytes = received
        self.total_bytes = total
        
        if total > 0:
            progress = int((received / total) * 100)
            self.progress_updated.emit(progress)
            
    def on_finished(self):
        """Handle download completion."""
        state = self.download_request.state()
        if state == QWebEngineDownloadRequest.DownloadState.DownloadCompleted:
            self.state = "completed"
            self.download_finished.emit(True)
        else:
            self.state = "failed"
            self.download_finished.emit(False)
            
    def cancel_download(self):
        """Cancel the download."""
        if self.download_request.state() == QWebEngineDownloadRequest.DownloadState.DownloadInProgress:
            self.download_request.cancel()
            self.state = "cancelled"
            
    def get_info_dict(self):
        """Get download information as dictionary."""
        return {
            "file_name": self.file_name,
            "file_path": self.file_path,
            "total_bytes": self.total_bytes,
            "received_bytes": self.received_bytes,
            "state": self.state,
            "start_time": self.start_time.isoformat(),
            "url": self.download_request.url().toString()
        }


class DownloadManager(QObject):
    """Manages all downloads."""
    
    download_added = pyqtSignal(object)  # DownloadItem
    
    def __init__(self):
        super().__init__()
        self.downloads = []
        self.downloads_file = os.path.join(os.path.expanduser("~"), ".secure_browser_downloads.json")
        self.load_download_history()
        
    def download_requested(self, download_request):
        """Handle new download requests."""
        download_item = DownloadItem(download_request)
        self.downloads.append(download_item)
        
        # Connect signals
        download_item.download_finished.connect(lambda success: self.save_download_history())
        
        # Start download
        download_item.start_download()
        self.download_added.emit(download_item)
        
    def get_downloads(self):
        """Get all download items."""
        return self.downloads.copy()
        
    def get_active_downloads(self):
        """Get currently active downloads."""
        return [d for d in self.downloads if d.state == "downloading"]
        
    def cancel_download(self, download_item):
        """Cancel a specific download."""
        download_item.cancel_download()
        
    def remove_download(self, download_item):
        """Remove a download from the list."""
        if download_item in self.downloads:
            self.downloads.remove(download_item)
            self.save_download_history()
            
    def clear_completed_downloads(self):
        """Clear all completed downloads from the list."""
        self.downloads = [d for d in self.downloads if d.state not in ["completed", "failed", "cancelled"]]
        self.save_download_history()
        
    def load_download_history(self):
        """Load download history from file."""
        try:
            if os.path.exists(self.downloads_file):
                with open(self.downloads_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    # Note: Only load metadata, not active downloads
                    return history
        except Exception as e:
            print(f"Error loading download history: {e}")
        return []
        
    def save_download_history(self):
        """Save download history to file."""
        try:
            history = []
            for download in self.downloads:
                if download.state in ["completed", "failed"]:
                    history.append(download.get_info_dict())
                    
            with open(self.downloads_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving download history: {e}")
            
    def show_downloads_dialog(self, parent):
        """Show downloads management dialog."""
        dialog = DownloadsDialog(self, parent)
        dialog.exec()


class DownloadsDialog(QDialog):
    """Dialog for managing downloads."""
    
    def __init__(self, download_manager, parent=None):
        super().__init__(parent)
        self.download_manager = download_manager
        self.download_widgets = {}
        self.init_ui()
        self.load_downloads_list()
        self.setup_update_timer()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Downloads")
        self.setGeometry(200, 200, 700, 500)
        
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("Downloads")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header_label)
        
        # Downloads list
        self.downloads_list = QListWidget()
        layout.addWidget(self.downloads_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        open_folder_btn = QPushButton("Open Downloads Folder")
        open_folder_btn.clicked.connect(self.open_downloads_folder)
        button_layout.addWidget(open_folder_btn)
        
        clear_btn = QPushButton("Clear Completed")
        clear_btn.clicked.connect(self.clear_completed)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def setup_update_timer(self):
        """Setup timer for updating download progress."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_progress)
        self.update_timer.start(1000)  # Update every second
        
    def load_downloads_list(self):
        """Load downloads into the list widget."""
        self.downloads_list.clear()
        self.download_widgets.clear()
        
        for download in self.download_manager.get_downloads():
            self.add_download_widget(download)
            
    def add_download_widget(self, download_item):
        """Add a download widget to the list."""
        widget = DownloadWidget(download_item)
        list_item = QListWidgetItem()
        list_item.setSizeHint(widget.sizeHint())
        
        self.downloads_list.addItem(list_item)
        self.downloads_list.setItemWidget(list_item, widget)
        
        self.download_widgets[download_item] = (list_item, widget)
        
    def update_progress(self):
        """Update progress for active downloads."""
        for download_item, (list_item, widget) in self.download_widgets.items():
            if download_item.state == "downloading":
                widget.update_progress()
                
    def clear_completed(self):
        """Clear completed downloads."""
        self.download_manager.clear_completed_downloads()
        self.load_downloads_list()
        
    def open_downloads_folder(self):
        """Open the downloads folder."""
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(downloads_dir):
            if os.name == 'nt':  # Windows
                os.startfile(downloads_dir)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{downloads_dir}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{downloads_dir}"')


class DownloadWidget(QWidget):
    """Widget for displaying a single download item."""
    
    def __init__(self, download_item):
        super().__init__()
        self.download_item = download_item
        self.init_ui()
        
    def init_ui(self):
        """Initialize the widget UI."""
        layout = QVBoxLayout(self)
        
        # File name and status
        info_layout = QHBoxLayout()
        self.name_label = QLabel(self.download_item.file_name)
        self.name_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self.name_label)
        
        info_layout.addStretch()
        
        self.status_label = QLabel(self.download_item.state.title())
        info_layout.addWidget(self.status_label)
        
        layout.addLayout(info_layout)
        
        # Progress bar
        if self.download_item.state == "downloading":
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            layout.addWidget(self.progress_bar)
            
        # URL
        url_label = QLabel(self.download_item.download_request.url().toString())
        url_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(url_label)
        
    def update_progress(self):
        """Update the progress bar."""
        if hasattr(self, 'progress_bar') and self.download_item.total_bytes > 0:
            progress = int((self.download_item.received_bytes / self.download_item.total_bytes) * 100)
            self.progress_bar.setValue(progress)
            
            # Update status
            received_mb = self.download_item.received_bytes / (1024 * 1024)
            total_mb = self.download_item.total_bytes / (1024 * 1024)
            self.status_label.setText(f"{received_mb:.1f} MB / {total_mb:.1f} MB")
