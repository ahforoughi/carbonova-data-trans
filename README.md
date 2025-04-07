# Excel File Monitor

A native Windows application that monitors Excel files for changes and syncs new rows to the cloud.

## Features

- Monitor Excel files for changes in real-time
- Automatic detection of new rows
- Cloud synchronization
- User-friendly interface with logging
- Easy deployment

## Installation

1. Ensure Python 3.8 or higher is installed on your system
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your cloud API credentials:
   ```
   CLOUD_API_URL=your_api_url
   CLOUD_API_KEY=your_api_key
   ```

## Usage

1. Run the application:
   ```
   python excel_monitor.py
   ```
2. Select an Excel file to monitor using the file picker
3. The application will automatically detect and sync new rows
4. View logs in the application window

## Deployment

To create a standalone executable:
1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Build the executable:
   ```
   pyinstaller --onefile --windowed excel_monitor.py
   ```
3. The executable will be created in the `dist` directory

## Requirements

- Windows 10 or higher
- Python 3.8 or higher
- Internet connection for cloud sync 