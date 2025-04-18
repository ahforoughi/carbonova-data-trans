# Excel Monitor

A professional Windows application that monitors Excel files for changes and automatically syncs new data to the cloud. Built with security and ease of use in mind.

## Features

- **File Monitoring**
  - Supports multiple Excel formats (xlsx, xls, csv, xlsm, xlsb)
  - Real-time change detection
  - Automatic row detection and syncing
  - Handles large files efficiently

- **Security**
  - Password protection
  - Secure storage of API credentials
  - Encrypted settings storage
  - Protected log files

- **Cloud Integration**
  - Configurable API endpoints
  - Secure API key management
  - Automatic data synchronization
  - Error handling and retry logic

- **User Interface**
  - Modern dark mode design
  - Real-time activity logging
  - Status indicators
  - Intuitive file selection
  - Easy-to-use settings panel

- **Logging**
  - Detailed activity logs
  - Error tracking
  - Configurable log file location
  - Timestamp for all events

## Installation

### Quick Install
1. Go to the [Releases](https://github.com/yourusername/excel-monitor/releases) page
2. Download the latest release `ExcelMonitor.exe`
3. Double-click to run the application
4. On first run, you'll be prompted to set a password
5. Use the Settings button to configure your Cloud API settings

### System Requirements
- Windows 10 or higher
- 4GB RAM minimum
- 100MB free disk space
- Internet connection for cloud sync
- Excel files should not be open in other programs while monitoring

## Usage Guide

### First Time Setup
1. Launch ExcelMonitor.exe
2. Create a password when prompted (minimum 6 characters)
3. Click the Settings button (gear icon)
4. Configure your Cloud API settings:
   - Enter your API URL
   - Enter your API Key
   - Configure log file settings
5. Click Save to store your settings

### Monitoring Files
1. Click "Select File" to choose an Excel file
2. The application will automatically:
   - Start monitoring the file
   - Detect any changes
   - Sync new rows to the cloud
   - Display activity in the log
3. The status indicator will show the current monitoring state

### Settings Management
1. Click the Settings button to access:
   - Cloud API configuration
   - Log file settings
   - Password management
2. Changes take effect immediately
3. Settings are saved securely in the Windows registry

### Log Management
1. Logs are displayed in real-time in the application
2. Log files are saved to your specified location
3. Each log entry includes:
   - Timestamp
   - Event type
   - Detailed message
   - Error information (if applicable)

## Troubleshooting

### Common Issues
1. **File Access Errors**
   - Ensure the Excel file is not open in another program
   - Check file permissions
   - Verify the file path is accessible

2. **Cloud Sync Issues**
   - Verify your internet connection
   - Check API credentials in Settings
   - Ensure the API endpoint is correct
   - Check the logs for specific error messages

3. **Application Not Responding**
   - Check the log files for errors
   - Ensure sufficient system resources
   - Try restarting the application

### Log File Location
- Default: `%USERPROFILE%\Documents\ExcelMonitor\logs`
- Custom location can be set in Settings

## Support

For additional support:
1. Check the log files for detailed error messages
2. Verify your system meets the requirements
3. Ensure all settings are correctly configured
4. Contact support with the following information:
   - Error messages from logs
   - System specifications
   - Steps to reproduce the issue

## Security Notes

- Passwords are stored securely in the Windows registry
- API keys are encrypted
- Log files contain sensitive information - handle with care
- Regular password updates are recommended
- Keep your API credentials secure

## Updates

### Automatic Updates
The application will check for updates when launched. To update:
1. Download the new version from the [Releases](https://github.com/yourusername/excel-monitor/releases) page
2. Close the current application
3. Replace the old executable with the new one
4. Launch the updated version

### Release Notes
Each release includes:
- Version number
- Release date
- List of changes
- Known issues
- Installation instructions

## Development

### Building from Source
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate the icon:
   ```bash
   python app_icon.py
   ```
4. Build the executable:
   ```bash
   python build.py
   ```

### Running Tests
1. Install test dependencies:
   ```bash
   pip install pytest pytest-qt
   ```
2. Run all tests:
   ```bash
   python run_tests.py
   ```
3. Run specific test files:
   ```bash
   python -m pytest tests/test_file_handler.py
   ```

### Test Coverage
The application includes comprehensive unit tests for:
- File handling and monitoring
- Cloud synchronization
- Settings management
- Login functionality
- UI components

Tests are automatically run on pull requests and before releases.

### Creating a Release
1. Update version in `setup.py`
2. Create and push a new tag:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
3. GitHub Actions will automatically:
   - Run all tests
   - Build the executable
   - Create a release
   - Upload the executable
   - Generate release notes

## License

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited. 