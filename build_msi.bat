@echo off
REM Bhaarat Browser Installer Builder
REM Created by: Devesh Kumar
REM Copyright © 2025 Devesh Kumar. All rights reserved.

echo ==========================================
echo  Bhaarat Browser v1.0.1 Installer Builder
echo  Created by: Devesh Kumar
echo ==========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/4] Installing required dependencies...
echo Installing PyQt6 and build tools...
py -m pip install --upgrade pip
py -m pip install PyQt6 PyQt6-WebEngine PyQt6-sip PyQt6-Qt6 PyQt6-WebEngine-Qt6 cx_Freeze

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [3/4] Building MSI installer...
py setup.py bdist_msi

if errorlevel 1 (
    echo ERROR: Failed to build MSI installer
    pause
    exit /b 1
)
echo ✓ MSI installer built successfully

echo.
echo [4/4] Verifying installer...
if exist "dist\BhaaratBrowser-1.0.1-win64.msi" (
    echo ✓ Installer created: dist\BhaaratBrowser-1.0.1-win64.msi
    dir "dist\BhaaratBrowser-1.0.1-win64.msi"
) else (
    echo ERROR: Installer not found in dist folder
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Build Complete! 
echo  Created by: Devesh Kumar
echo ==========================================
echo.
echo Your MSI installer is ready:
echo Location: dist\BhaaratBrowser-1.0.1-win64.msi
echo Size: ~177 MB
echo.
echo You can now:
echo 1. Install the browser by running the MSI file
echo 2. Share the MSI file with others
echo 3. Upload to cloud storage for distribution
echo.
pause
