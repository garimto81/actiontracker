@echo off
echo ========================================
echo Action Tracker Build Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Installing required dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.pyc" del /q "*.pyc"

echo.
echo [3/5] Building executable with PyInstaller...
pyinstaller --clean ActionTracker.spec
if %errorlevel% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo.
echo [4/5] Copying additional files to dist folder...
if not exist "dist" mkdir "dist"
xcopy /y "*.json" "dist\" >nul 2>&1
xcopy /y "*.csv" "dist\" >nul 2>&1
xcopy /y "*.md" "dist\docs\" >nul 2>&1
if not exist "dist\docs" mkdir "dist\docs"

echo.
echo [5/5] Build completed successfully!
echo.
echo ========================================
echo Executable location: dist\ActionTracker.exe
echo ========================================
echo.
echo Press any key to exit...
pause >nul