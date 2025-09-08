@echo off
REM Build script for Bhaarat Browser

echo ========================================
echo Building Bhaarat Browser
echo ========================================

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Creating executable...
py setup.py build

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create executable!
    pause
    exit /b 1
)

echo.
echo Creating MSI installer...
py setup.py bdist_msi

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create MSI installer!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: build\exe.win-amd64-3.11\BhaaratBrowser.exe
echo MSI installer location: dist\BhaaratBrowser-1.0.0-amd64.msi
echo.
echo To install the browser, run the MSI file as administrator.
echo.
pause
