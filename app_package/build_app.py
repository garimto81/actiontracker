"""
Build script for Action Tracker Automation
Creates standalone executables for different platforms
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

class AppBuilder:
    def __init__(self):
        self.app_name = "ActionTrackerAutomation"
        self.version = "2.0.0"
        self.root_dir = Path(__file__).parent
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        
    def clean_build(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
        print("✅ Clean complete")
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        
        # Install Python dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", 
            str(self.root_dir / "backend" / "requirements.txt")
        ], check=True)
        
        # Install PyInstaller
        subprocess.run([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ], check=True)
        
        # Install Node dependencies
        subprocess.run(["npm", "install"], cwd=self.root_dir, check=True)
        
        print("✅ Dependencies installed")
    
    def build_backend(self):
        """Build Python backend with PyInstaller"""
        print("🐍 Building Python backend...")
        
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['backend/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend/settings.json', 'backend'),
    ],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'fastapi',
        'pydantic',
        'pyautogui',
        'PIL',
        'cv2',
        'pandas',
        'numpy',
        'win32gui',
        'win32con',
        'websockets'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='action_tracker_backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='assets/icon.ico'
)
'''
        
        # Write spec file
        spec_path = self.root_dir / "backend.spec"
        spec_path.write_text(spec_content)
        
        # Create version info
        version_info = f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.version.replace(".", ", ")}, 0),
    prodvers=({self.version.replace(".", ", ")}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'ActionTracker Team'),
        StringStruct(u'FileDescription', u'Action Tracker Automation Backend'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'action_tracker_backend'),
        StringStruct(u'LegalCopyright', u'© 2025 ActionTracker Team'),
        StringStruct(u'OriginalFilename', u'action_tracker_backend.exe'),
        StringStruct(u'ProductName', u'Action Tracker Automation'),
        StringStruct(u'ProductVersion', u'{self.version}')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        version_path = self.root_dir / "version_info.txt"
        version_path.write_text(version_info)
        
        # Run PyInstaller
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            str(spec_path)
        ], check=True)
        
        print("✅ Backend build complete")
    
    def build_electron(self, platform="all"):
        """Build Electron app for specified platform"""
        print(f"⚡ Building Electron app for {platform}...")
        
        if platform == "all":
            subprocess.run(["npm", "run", "build-all"], cwd=self.root_dir, check=True)
        elif platform == "windows":
            subprocess.run(["npm", "run", "build-win"], cwd=self.root_dir, check=True)
        elif platform == "mac":
            subprocess.run(["npm", "run", "build-mac"], cwd=self.root_dir, check=True)
        elif platform == "linux":
            subprocess.run(["npm", "run", "build-linux"], cwd=self.root_dir, check=True)
        
        print(f"✅ Electron build complete for {platform}")
    
    def create_portable(self):
        """Create portable version"""
        print("📦 Creating portable version...")
        
        portable_dir = self.dist_dir / f"{self.app_name}_Portable_{self.version}"
        portable_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy backend executable
        backend_exe = self.dist_dir / "action_tracker_backend.exe"
        if backend_exe.exists():
            shutil.copy2(backend_exe, portable_dir / "backend.exe")
        
        # Copy Electron files
        electron_dist = self.dist_dir / "win-unpacked"
        if electron_dist.exists():
            shutil.copytree(electron_dist, portable_dir / "app", dirs_exist_ok=True)
        
        # Create launch script
        launch_script = '''@echo off
echo Starting Action Tracker Automation...
start "" "backend.exe"
timeout /t 3 /nobreak > nul
start "" "app\\Action Tracker Automation.exe"
'''
        
        (portable_dir / "Launch.bat").write_text(launch_script)
        
        # Create README
        readme_content = f'''
# Action Tracker Automation Portable v{self.version}

## Quick Start
1. Extract all files to a folder
2. Run Launch.bat to start the application
3. The application will open in your default browser

## Requirements
- Windows 10 or later
- 1920x1080 display resolution recommended

## Features
- Cross-platform automation system
- Google Sheets integration
- Real-time player management
- Multiple speed modes

## Support
Visit: https://github.com/yourusername/action-tracker-automation
'''
        
        (portable_dir / "README.txt").write_text(readme_content)
        
        # Create ZIP archive
        shutil.make_archive(
            str(self.dist_dir / f"{self.app_name}_Portable_{self.version}"),
            'zip',
            portable_dir
        )
        
        print(f"✅ Portable version created: {self.app_name}_Portable_{self.version}.zip")
    
    def build_all(self):
        """Build everything"""
        print(f"🚀 Building {self.app_name} v{self.version}")
        print("=" * 50)
        
        self.clean_build()
        self.install_dependencies()
        self.build_backend()
        self.build_electron("windows")
        self.create_portable()
        
        print("=" * 50)
        print("✨ Build complete!")
        print(f"📁 Output directory: {self.dist_dir}")
        
        # List created files
        print("\n📦 Created packages:")
        for file in self.dist_dir.glob("*"):
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"  - {file.name} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    builder = AppBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clean":
            builder.clean_build()
        elif command == "backend":
            builder.build_backend()
        elif command == "electron":
            platform = sys.argv[2] if len(sys.argv) > 2 else "all"
            builder.build_electron(platform)
        elif command == "portable":
            builder.create_portable()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python build_app.py [clean|backend|electron|portable|all]")
    else:
        builder.build_all()