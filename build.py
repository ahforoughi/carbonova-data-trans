import PyInstaller.__main__
import os
import shutil

# Clean previous builds
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Create executable
PyInstaller.__main__.run([
    'main.py',
    '--name=ExcelMonitor',
    '--onefile',
    '--windowed',
    '--icon=app_icon.ico',
    '--add-data=README.md;.',
    '--noconsole',
    '--clean',
]) 