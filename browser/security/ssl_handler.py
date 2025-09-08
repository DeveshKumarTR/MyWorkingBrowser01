"""
SSL Handler - Handle SSL/TLS certificate validation and security.

This module provides SSL certificate validation, security warnings,
and secure connection management for the browser.
"""

import ssl
import socket
import certifi
from urllib.parse import urlparse
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox


class SSLHandler(QObject):
    """Handles SSL/TLS security validation."""
    
    ssl_error = pyqtSignal(str, str)  # URL, error message
    ssl_warning = pyqtSignal(str, str)  # URL, warning message
    
    def __init__(self):
        super().__init__()
        self.trusted_certificates = set()
        self.untrusted_certificates = set()
        
    def validate_ssl_certificate(self, url):
        """Validate SSL certificate for the given URL."""
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme != 'https':
                return True  # No SSL validation needed for non-HTTPS
                
            hostname = parsed_url.hostname
            port = parsed_url.port or 443
            
            # Create SSL context with proper verification
            context = ssl.create_default_context(cafile=certifi.where())
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Connect and verify certificate
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    return self.validate_certificate_details(cert, hostname)
                    
        except ssl.SSLError as e:
            self.ssl_error.emit(url, f"SSL Error: {str(e)}")
            return False
        except Exception as e:
            self.ssl_error.emit(url, f"Connection Error: {str(e)}")
            return False
            
    def validate_certificate_details(self, cert, hostname):
        """Validate certificate details."""
        if not cert:
            return False
            
        try:
            # Check if certificate is expired
            import datetime
            not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            if not_after < datetime.datetime.now():
                return False
                
            # Check subject alternative names
            san_list = []
            for san in cert.get('subjectAltName', []):
                if san[0] == 'DNS':
                    san_list.append(san[1])
                    
            # Check if hostname matches certificate
            subject = dict(x[0] for x in cert['subject'])
            common_name = subject.get('commonName', '')
            
            if hostname in san_list or hostname == common_name:
                return True
                
            # Check for wildcard match
            for san in san_list:
                if san.startswith('*.') and hostname.endswith(san[2:]):
                    return True
                    
            return False
            
        except Exception:
            return False
            
    def get_certificate_info(self, url):
        """Get detailed certificate information."""
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme != 'https':
                return None
                
            hostname = parsed_url.hostname
            port = parsed_url.port or 443
            
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'subject_alt_name': cert.get('subjectAltName', [])
                    }
                    
        except Exception as e:
            return {'error': str(e)}
            
    def is_secure_connection(self, url):
        """Check if the connection is secure."""
        parsed_url = urlparse(url)
        return parsed_url.scheme == 'https'
        
    def get_security_level(self, url):
        """Get security level for the URL."""
        if not self.is_secure_connection(url):
            return 'insecure'
            
        if self.validate_ssl_certificate(url):
            return 'secure'
        else:
            return 'warning'
            
    def show_certificate_details(self, url, parent=None):
        """Show certificate details dialog."""
        cert_info = self.get_certificate_info(url)
        
        if not cert_info:
            QMessageBox.information(parent, "Certificate Info", "No certificate information available.")
            return
            
        if 'error' in cert_info:
            QMessageBox.warning(parent, "Certificate Error", f"Error getting certificate: {cert_info['error']}")
            return
            
        # Format certificate information
        details = []
        details.append(f"Subject: {cert_info['subject'].get('commonName', 'N/A')}")
        details.append(f"Issuer: {cert_info['issuer'].get('commonName', 'N/A')}")
        details.append(f"Valid From: {cert_info['not_before']}")
        details.append(f"Valid Until: {cert_info['not_after']}")
        details.append(f"Serial Number: {cert_info['serial_number']}")
        
        if cert_info['subject_alt_name']:
            san_names = [san[1] for san in cert_info['subject_alt_name'] if san[0] == 'DNS']
            details.append(f"Subject Alternative Names: {', '.join(san_names)}")
            
        message = "\n".join(details)
        QMessageBox.information(parent, f"Certificate Details - {urlparse(url).hostname}", message)
        
    def check_mixed_content(self, main_url, resource_urls):
        """Check for mixed content (HTTP resources on HTTPS page)."""
        if not self.is_secure_connection(main_url):
            return []  # No mixed content issues for non-HTTPS pages
            
        mixed_content = []
        for resource_url in resource_urls:
            if not self.is_secure_connection(resource_url):
                mixed_content.append(resource_url)
                
        return mixed_content
