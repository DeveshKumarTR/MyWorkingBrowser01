#!/usr/bin/env python3
"""
Bhaarat Browser Installer Builder
Created by: Devesh Kumar
Copyright © 2025 Devesh Kumar. All rights reserved.

This script automates the process of building the MSI installer
for Bhaarat Browser on Windows systems.
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    print("=" * 50)
    print("  Bhaarat Browser v1.0.1 Installer Builder")
    print("  Created by: Devesh Kumar")
    print("=" * 50)
    print()

def check_python():
    print("[1/4] Checking Python installation...")
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
            return True
        else:
            print(f"✗ Python {version.major}.{version.minor} found, but 3.8+ required")
            return False
    except Exception as e:
        print(f"✗ Error checking Python: {e}")
        return False

def install_dependencies():
    print("\n[2/4] Installing required dependencies...")
    dependencies = [
        "PyQt6",
        "PyQt6-WebEngine", 
        "PyQt6-sip",
        "PyQt6-Qt6",
        "PyQt6-WebEngine-Qt6",
        "cx_Freeze"
    ]
    
    try:
        print("Installing dependencies...")
        for dep in dependencies:
            print(f"  Installing {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", dep
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"✗ Failed to install {dep}")
                print(result.stderr)
                return False
        
        print("✓ All dependencies installed successfully")
        return True
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def build_msi():
    print("\n[3/4] Building MSI installer...")
    try:
        result = subprocess.run([
            sys.executable, "setup.py", "bdist_msi"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ MSI installer built successfully")
            return True
        else:
            print("✗ Failed to build MSI installer")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error building MSI: {e}")
        return False

def verify_installer():
    print("\n[4/4] Verifying installer...")
    msi_path = Path("dist/BhaaratBrowser-1.0.1-win64.msi")
    
    if msi_path.exists():
        size_mb = msi_path.stat().st_size / (1024 * 1024)
        print(f"✓ Installer created: {msi_path}")
        print(f"  Size: {size_mb:.1f} MB")
        return True
    else:
        print("✗ Installer not found in dist folder")
        return False

def print_completion():
    print("\n" + "=" * 50)
    print("  Build Complete!")
    print("  Created by: Devesh Kumar") 
    print("=" * 50)
    print("\nYour MSI installer is ready:")
    print("Location: dist/BhaaratBrowser-1.0.1-win64.msi")
    print("Size: ~177 MB")
    print("\nYou can now:")
    print("1. Install the browser by running the MSI file")
    print("2. Share the MSI file with others") 
    print("3. Upload to cloud storage for distribution")

def main():
    print_header()
    
    if not check_python():
        print("\nPlease install Python 3.8+ from https://python.org")
        return 1
    
    if not install_dependencies():
        print("\nFailed to install dependencies")
        return 1
    
    if not build_msi():
        print("\nFailed to build MSI installer")
        return 1
    
    if not verify_installer():
        print("\nFailed to verify installer")
        return 1
    
    print_completion()
    return 0

if __name__ == "__main__":
    sys.exit(main())
