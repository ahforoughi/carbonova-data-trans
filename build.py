import PyInstaller.__main__
import os
import shutil
import sys

def build_executable():
    print("Starting build process...")
    
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    print("Building executable...")
    try:
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
        
        # Verify the executable was created
        exe_path = os.path.join('dist', 'ExcelMonitor.exe')
        if os.path.exists(exe_path):
            print(f"Successfully created executable at: {exe_path}")
            print(f"File size: {os.path.getsize(exe_path) / 1024 / 1024:.2f} MB")
        else:
            print("Error: Executable was not created!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error during build: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable() 