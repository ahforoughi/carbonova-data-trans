import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time
from PySide6.QtCore import QTimer

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.last_row_count = 0
        self.last_modified = 0
        self.observer = None
        self.watched_file = None
        self.last_content = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_file)
        self.polling_interval = 1000  # Check every second
    
    def read_excel_file(self, file_path):
        """Read Excel file with appropriate engine"""
        try:
            if file_path.endswith('.xlsx'):
                return pd.read_excel(file_path, engine='openpyxl')
            elif file_path.endswith('.xls'):
                return pd.read_excel(file_path, engine='xlrd')
            elif file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.xlsm'):
                return pd.read_excel(file_path, engine='openpyxl')
            elif file_path.endswith('.xlsb'):
                return pd.read_excel(file_path, engine='pyxlsb')
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def start_watching(self, file_path):
        """Start watching the specified file for changes"""
        print(f"Starting to watch file: {file_path}")
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        self.watched_file = file_path
        self.observer = Observer()
        
        # Watch the directory containing the file
        directory = os.path.dirname(file_path)
        print(f"Watching directory: {directory}")
        
        self.observer.schedule(self, directory, recursive=False)
        self.observer.start()
        
        # Set initial state
        df = self.read_excel_file(file_path)
        if df is not None:
            self.last_row_count = len(df)
            self.last_content = df
            print(f"Initial row count: {self.last_row_count}")
        
        # Start polling timer
        self.timer.start(self.polling_interval)
    
    def stop(self):
        """Stop watching the file"""
        if self.observer:
            print("Stopping file watcher")
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.watched_file = None
            self.last_content = None
        
        # Stop polling timer
        self.timer.stop()
    
    def check_file(self):
        """Check the file for changes"""
        if not self.watched_file or not os.path.exists(self.watched_file):
            return
        
        try:
            # Get current file modification time
            current_mtime = os.path.getmtime(self.watched_file)
            
            # Only check if file has been modified
            if current_mtime > self.last_modified:
                self.last_modified = current_mtime
                
                # Read the Excel file
                df = self.read_excel_file(self.watched_file)
                if df is None:
                    print("Failed to read file")
                    return
                
                current_row_count = len(df)
                print(f"Current row count: {current_row_count}, Last row count: {self.last_row_count}")
                
                # Check if there are new rows
                if current_row_count > self.last_row_count:
                    # Get the new rows
                    new_rows = df.iloc[self.last_row_count:].to_dict('records')
                    print(f"Found {len(new_rows)} new rows:")
                    
                    # Print each new row's content
                    for i, row in enumerate(new_rows, start=self.last_row_count + 1):
                        print(f"Row {i}: {row}")
                    
                    # Update the last content and row count
                    self.last_content = df
                    self.last_row_count = current_row_count
                    
                    # Call the callback with new rows
                    self.callback(new_rows)
                else:
                    print("No new rows detected")
        
        except Exception as e:
            print(f"Error checking file: {e}")
            import traceback
            traceback.print_exc()
    
    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory and event.src_path == self.watched_file:
            print(f"File modified: {event.src_path}")
            # The polling mechanism will handle the actual change detection
    
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory and event.src_path == self.watched_file:
            print(f"File created: {event.src_path}")
            self.start_watching(event.src_path)
    
    def on_deleted(self, event):
        """Handle file deletion events"""
        if not event.is_directory and event.src_path == self.watched_file:
            print(f"File deleted: {event.src_path}")
            self.stop() 