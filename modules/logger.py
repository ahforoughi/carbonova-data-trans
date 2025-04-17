import os
import logging
from datetime import datetime
import sys

class Logger:
    def __init__(self):
        # Get the directory where the executable is running
        if getattr(sys, 'frozen', False):
            # If running as compiled executable
            base_dir = os.path.dirname(sys.executable)
        else:
            # If running as script
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create logs directory in the same location as the executable
        self.log_dir = os.path.join(base_dir, "logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Set log file path
        self.log_file = os.path.join(self.log_dir, "excel_monitor.log")
        
        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger('ExcelMonitor')
    
    def log(self, message):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info(f"{timestamp} - {message}") 