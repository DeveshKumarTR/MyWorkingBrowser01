#!/bin/bash
# Build script for Bhaarat Browser (Linux/Mac)

echo "========================================"
echo "Building Bhaarat Browser"
echo "========================================"

# Clean previous builds
rm -rf build dist

echo ""
echo "Creating executable..."
python setup.py build

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create executable!"
    exit 1
fi

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo ""
echo "Executable location: build/exe.linux-x86_64-3.x/BhaaratBrowser"
echo ""
echo "To run the browser, execute the file in the build directory."
echo ""
