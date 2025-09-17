@echo off
echo ========================================
echo Action Tracker Portable Build Script
echo ========================================
echo.
echo This script creates a portable folder version
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/6] Installing required dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/6] Creating alternative spec file for folder output...
:: Create a folder output spec file
echo # -*- mode: python ; coding: utf-8 -*- > ActionTracker_folder.spec
echo import sys >> ActionTracker_folder.spec
echo import os >> ActionTracker_folder.spec
echo from PyInstaller.utils.hooks import collect_data_files, collect_submodules >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo block_cipher = None >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo datas = [ >> ActionTracker_folder.spec
echo     ('*.json', '.'), >> ActionTracker_folder.spec
echo     ('*.csv', '.'), >> ActionTracker_folder.spec
echo     ('*.bat', '.'), >> ActionTracker_folder.spec
echo     ('*.md', 'docs'), >> ActionTracker_folder.spec
echo ] >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo hiddenimports = [ >> ActionTracker_folder.spec
echo     'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', >> ActionTracker_folder.spec
echo     'pyautogui', 'pandas', 'numpy', 'requests', 'PIL', 'PIL.Image', >> ActionTracker_folder.spec
echo     'PIL.ImageGrab', 'cv2', 'keyboard', 'threading', 'json', 'csv', >> ActionTracker_folder.spec
echo     'io', 'datetime', 'time', 'os', 'sys', >> ActionTracker_folder.spec
echo ] >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo if sys.platform == 'win32': >> ActionTracker_folder.spec
echo     hiddenimports.extend(['win32gui', 'win32con', 'win32api', 'win32process', 'pywintypes']) >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo a = Analysis( >> ActionTracker_folder.spec
echo     ['integrated_gui_final.py'], >> ActionTracker_folder.spec
echo     pathex=[], >> ActionTracker_folder.spec
echo     binaries=[], >> ActionTracker_folder.spec
echo     datas=datas, >> ActionTracker_folder.spec
echo     hiddenimports=hiddenimports, >> ActionTracker_folder.spec
echo     hookspath=[], >> ActionTracker_folder.spec
echo     hooksconfig={}, >> ActionTracker_folder.spec
echo     runtime_hooks=[], >> ActionTracker_folder.spec
echo     excludes=['matplotlib', 'scipy', 'jupyter', 'notebook', 'pytest', 'setuptools', 'pip'], >> ActionTracker_folder.spec
echo     win_no_prefer_redirects=False, >> ActionTracker_folder.spec
echo     win_private_assemblies=False, >> ActionTracker_folder.spec
echo     cipher=block_cipher, >> ActionTracker_folder.spec
echo     noarchive=False, >> ActionTracker_folder.spec
echo ) >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher) >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo exe = EXE( >> ActionTracker_folder.spec
echo     pyz, >> ActionTracker_folder.spec
echo     a.scripts, >> ActionTracker_folder.spec
echo     [], >> ActionTracker_folder.spec
echo     exclude_binaries=True, >> ActionTracker_folder.spec
echo     name='ActionTracker', >> ActionTracker_folder.spec
echo     debug=False, >> ActionTracker_folder.spec
echo     bootloader_ignore_signals=False, >> ActionTracker_folder.spec
echo     strip=False, >> ActionTracker_folder.spec
echo     upx=True, >> ActionTracker_folder.spec
echo     console=False, >> ActionTracker_folder.spec
echo     disable_windowed_traceback=False, >> ActionTracker_folder.spec
echo     argv_emulation=False, >> ActionTracker_folder.spec
echo     target_arch=None, >> ActionTracker_folder.spec
echo     codesign_identity=None, >> ActionTracker_folder.spec
echo     entitlements_file=None, >> ActionTracker_folder.spec
echo ) >> ActionTracker_folder.spec
echo. >> ActionTracker_folder.spec
echo coll = COLLECT( >> ActionTracker_folder.spec
echo     exe, >> ActionTracker_folder.spec
echo     a.binaries, >> ActionTracker_folder.spec
echo     a.zipfiles, >> ActionTracker_folder.spec
echo     a.datas, >> ActionTracker_folder.spec
echo     strip=False, >> ActionTracker_folder.spec
echo     upx=True, >> ActionTracker_folder.spec
echo     upx_exclude=[], >> ActionTracker_folder.spec
echo     name='ActionTracker_Portable' >> ActionTracker_folder.spec
echo ) >> ActionTracker_folder.spec

echo.
echo [3/6] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.pyc" del /q "*.pyc"

echo.
echo [4/6] Building portable folder with PyInstaller...
pyinstaller --clean ActionTracker_folder.spec
if %errorlevel% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo.
echo [5/6] Copying additional files to portable folder...
xcopy /y "*.json" "dist\ActionTracker_Portable\" >nul 2>&1
xcopy /y "*.csv" "dist\ActionTracker_Portable\" >nul 2>&1
if not exist "dist\ActionTracker_Portable\docs" mkdir "dist\ActionTracker_Portable\docs"
xcopy /y "*.md" "dist\ActionTracker_Portable\docs\" >nul 2>&1

echo.
echo [6/6] Creating launch script...
echo @echo off > "dist\ActionTracker_Portable\Launch_ActionTracker.bat"
echo cd /d "%%~dp0" >> "dist\ActionTracker_Portable\Launch_ActionTracker.bat"
echo start ActionTracker.exe >> "dist\ActionTracker_Portable\Launch_ActionTracker.bat"

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Portable folder location: dist\ActionTracker_Portable\
echo To run: Execute Launch_ActionTracker.bat
echo.
echo The folder can be copied to any Windows computer
echo and run without Python installation.
echo ========================================
echo.
echo Press any key to exit...
pause >nul