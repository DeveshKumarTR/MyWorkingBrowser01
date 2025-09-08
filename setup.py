#!/usr/bin/env python
"""
Setup script for building Bhaarat Browser executable and MSI installer.
"""

import sys
from cx_Freeze import setup, Executable
import os

# Build options
build_options = {
    'packages': [
        'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 
        'PyQt6.QtWebEngineWidgets', 'PyQt6.QtWebEngineCore',
        'json', 'os', 'datetime', 'urllib', 'ssl', 'socket',
        'certifi', 'requests', 'cryptography', 'validators'
    ],
    'excludes': [
        'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy',
        'IPython', 'jupyter', 'notebook'
    ],
    'include_files': [
        ('README.md', 'README.md'),
        ('requirements.txt', 'requirements.txt'),
    ],
    'zip_include_packages': ['*'],
    'zip_exclude_packages': []
}

# Base for console or GUI application
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Hide console window

# Define the executable
executables = [
    Executable(
        script="secure_browser.py",
        base=base,
        target_name="BhaaratBrowser.exe",
        icon=None,  # You can add an icon file here if you have one
        copyright="Copyright (C) 2025 Bhaarat Browser",
        trademarks="Bhaarat Browser"
    )
]

# Setup configuration
setup(
    name="BhaaratBrowser",
    version="1.0.0",
    description="Bhaarat Browser - A secure web browser with modern functionality",
    long_description="Bhaarat Browser is a secure web browser application built with Python and PyQt6, featuring tabbed browsing, bookmark management, and modern web engine capabilities.",
    author="Bhaarat Browser Team",
    author_email="contact@bhaaratbrowser.com",
    url="https://github.com/bhaaratbrowser/bhaarat-browser",
    executables=executables,
    options={
        'build_exe': build_options,
        'bdist_msi': {
            'upgrade_code': '{12345678-1234-5678-ABCD-123456789012}',  # Unique GUID
            'add_to_path': False,
            'initial_target_dir': r'[ProgramFilesFolder]\Bhaarat Browser',
            'install_icon': None,  # You can add an icon file here
            'summary_data': {
                'author': 'Bhaarat Browser Team',
                'comments': 'Bhaarat Browser - Secure Web Browser',
                'keywords': 'browser;web;secure;internet;chrome;firefox'
            }
        }
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
