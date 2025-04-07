from setuptools import setup, find_packages

setup(
    name="ExcelMonitor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openpyxl',
        'watchdog',
        'PySide6==6.6.1',
        'requests'
    ],
    author="ExcelMonitor",
    description="An application to monitor Excel files and sync changes to cloud",
    python_requires='>=3.8',
) 