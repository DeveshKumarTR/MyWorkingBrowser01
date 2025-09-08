"""
Popup Blocker - Handle popup window blocking and management.

This module provides popup blocking functionality to prevent
unwanted popup windows and advertisements from opening.
"""

import re
from urllib.parse import urlparse
from PyQt6.QtCore import QObject, pyqtSignal


class PopupBlocker(QObject):
    """Handles popup window blocking."""
    
    popup_blocked = pyqtSignal(str, str)  # URL, reason
    popup_allowed = pyqtSignal(str)  # URL
    
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.whitelist = set()
        self.blacklist = set()
        self.setup_default_rules()
        
    def setup_default_rules(self):
        """Setup default popup blocking rules."""
        # Common popup patterns to block
        self.popup_patterns = [
            r'popup',
            r'pop-up',
            r'advertisement',
            r'ads\.',
            r'advert',
            r'banner',
            r'sponsored',
            r'promo',
            r'offer',
            r'deal',
            r'casino',
            r'gambling',
            r'adult',
            r'xxx',
            r'porn',
            r'malware',
            r'virus',
            r'scam',
            r'phishing'
        ]
        
        # Trusted domains that are allowed to open popups
        self.trusted_domains = {
            'google.com',
            'youtube.com',
            'github.com',
            'stackoverflow.com',
            'microsoft.com',
            'apple.com',
            'mozilla.org',
            'wikipedia.org'
        }
        
    def should_block_popup(self, source_url, popup_url=None):
        """Determine if a popup should be blocked."""
        if not self.enabled:
            return False
            
        try:
            source_domain = urlparse(source_url.toString() if hasattr(source_url, 'toString') else str(source_url)).netloc
            
            # Check whitelist first
            if self.is_whitelisted(source_domain):
                self.popup_allowed.emit(str(source_url))
                return False
                
            # Check blacklist
            if self.is_blacklisted(source_domain):
                self.popup_blocked.emit(str(source_url), "Domain blacklisted")
                return True
                
            # Check trusted domains
            if self.is_trusted_domain(source_domain):
                self.popup_allowed.emit(str(source_url))
                return False
                
            # Check popup patterns in URL
            if popup_url:
                popup_str = popup_url.toString() if hasattr(popup_url, 'toString') else str(popup_url)
                if self.contains_popup_patterns(popup_str):
                    self.popup_blocked.emit(popup_str, "Matches popup patterns")
                    return True
                    
            # Check source URL patterns
            source_str = source_url.toString() if hasattr(source_url, 'toString') else str(source_url)
            if self.contains_popup_patterns(source_str):
                self.popup_blocked.emit(source_str, "Source matches popup patterns")
                return True
                
            # Block popups from suspicious domains
            if self.is_suspicious_domain(source_domain):
                self.popup_blocked.emit(str(source_url), "Suspicious domain")
                return True
                
            # Default behavior: block most popups
            self.popup_blocked.emit(str(source_url), "Default popup blocking")
            return True
            
        except Exception as e:
            # In case of error, err on the side of blocking
            self.popup_blocked.emit(str(source_url), f"Error in popup detection: {e}")
            return True
            
    def is_whitelisted(self, domain):
        """Check if domain is in whitelist."""
        domain = domain.lower()
        return any(domain.endswith(white_domain) for white_domain in self.whitelist)
        
    def is_blacklisted(self, domain):
        """Check if domain is in blacklist."""
        domain = domain.lower()
        return any(domain.endswith(black_domain) for black_domain in self.blacklist)
        
    def is_trusted_domain(self, domain):
        """Check if domain is trusted."""
        domain = domain.lower()
        return any(domain.endswith(trusted_domain) for trusted_domain in self.trusted_domains)
        
    def contains_popup_patterns(self, url):
        """Check if URL contains popup patterns."""
        url_lower = url.lower()
        return any(re.search(pattern, url_lower) for pattern in self.popup_patterns)
        
    def is_suspicious_domain(self, domain):
        """Check if domain looks suspicious."""
        domain = domain.lower()
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',  # IP addresses
            r'[a-z]{10,}\.com',  # Very long random-looking domains
            r'.*-ads?[-\.].*',  # Contains "ad" or "ads"
            r'.*click.*',  # Contains "click"
            r'.*track.*',  # Contains "track"
            r'.*affiliate.*',  # Contains "affiliate"
        ]
        
        return any(re.search(pattern, domain) for pattern in suspicious_patterns)
        
    def add_to_whitelist(self, domain):
        """Add domain to whitelist."""
        self.whitelist.add(domain.lower())
        
    def remove_from_whitelist(self, domain):
        """Remove domain from whitelist."""
        self.whitelist.discard(domain.lower())
        
    def add_to_blacklist(self, domain):
        """Add domain to blacklist."""
        self.blacklist.add(domain.lower())
        
    def remove_from_blacklist(self, domain):
        """Remove domain from blacklist."""
        self.blacklist.discard(domain.lower())
        
    def enable_popup_blocking(self):
        """Enable popup blocking."""
        self.enabled = True
        
    def disable_popup_blocking(self):
        """Disable popup blocking."""
        self.enabled = False
        
    def is_enabled(self):
        """Check if popup blocking is enabled."""
        return self.enabled
        
    def get_blocking_stats(self):
        """Get popup blocking statistics."""
        # This would be implemented with proper tracking
        return {
            'total_blocked': 0,
            'blocked_today': 0,
            'whitelist_size': len(self.whitelist),
            'blacklist_size': len(self.blacklist)
        }
        
    def clear_lists(self):
        """Clear whitelist and blacklist."""
        self.whitelist.clear()
        self.blacklist.clear()
