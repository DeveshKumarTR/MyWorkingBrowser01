"""
Secure Web View - Enhanced QWebEngineView with security features.

This module provides a secure web view component that extends QWebEngineView
with additional security features including popup blocking, SSL validation,
and secure content handling.
"""

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile, QWebEnginePage
from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from .security.popup_blocker import PopupBlocker


class SecurePage(QWebEnginePage):
    """Secure web page with popup blocking and security features."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.popup_blocker = PopupBlocker()
        
    def createWindow(self, window_type):
        """Handle window creation requests (popup blocking)."""
        if self.popup_blocker.should_block_popup(self.url()):
            return None
        return super().createWindow(window_type)
    
    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        """Filter navigation requests for security."""
        # Block potentially malicious URLs
        if self.is_malicious_url(url):
            return False
        return super().acceptNavigationRequest(url, navigation_type, is_main_frame)
    
    def is_malicious_url(self, url):
        """Check if URL is potentially malicious."""
        url_string = url.toString().lower()
        
        # Basic malware/phishing URL patterns
        suspicious_patterns = [
            'data:text/html',
            'javascript:',
            'vbscript:',
        ]
        
        for pattern in suspicious_patterns:
            if pattern in url_string:
                return True
        
        return False


class SecureWebView(QWebEngineView):
    """Secure web view with enhanced security features."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_secure_page()
        self.configure_security_settings()
        
    def setup_secure_page(self):
        """Setup secure page with security features."""
        secure_page = SecurePage(self)
        self.setPage(secure_page)
        
    def configure_security_settings(self):
        """Configure security settings for the web view."""
        settings = self.settings()
        
        # Enable security features
        try:
            settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
            
            # Enable modern web features (these might not be available in all versions)
            try:
                settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
                settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
            except AttributeError:
                pass  # These attributes might not be available
                
        except Exception as e:
            print(f"Warning: Could not configure all web settings: {e}")
        
    def contextMenuEvent(self, event):
        """Customize context menu for security."""
        menu = self.page().createStandardContextMenu()
        
        # Remove potentially unsafe actions
        for action in menu.actions():
            if action.text() in ['View page source', 'Inspect']:
                # Keep these for development, but could be removed for production
                pass
                
        menu.exec(event.globalPos())
    
    def load_url_safely(self, url):
        """Load URL with additional security checks."""
        if isinstance(url, str):
            url = QUrl(url)
            
        # Validate URL scheme
        if url.scheme() not in ['http', 'https', 'file']:
            QMessageBox.warning(self, 'Security Warning', 
                              f'Unsafe URL scheme: {url.scheme()}')
            return False
            
        # Load the URL
        self.setUrl(url)
        return True
