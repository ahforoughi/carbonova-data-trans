from setuptools import setup, find_packages

setup(
    name="ExcelMonitor",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'pandas==2.1.0',
        'openpyxl==3.1.2',
        'watchdog==4.0.0',
        'PySide6==6.6.1',
        'requests==2.31.0',
        'python-dotenv==1.0.1'
    ],
    author="ExcelMonitor",
    description="An application to monitor Excel files and sync changes to cloud",
    python_requires='>=3.8',
) 