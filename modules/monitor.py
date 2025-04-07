import os
import time
from datetime import datetime
from typing import Optional

import pandas as pd
from PySide6.QtCore import QThread, Signal, QSettings
from watchdog.observers import Observer
import requests

from modules.file_handler import ExcelHandler

class ExcelMonitor(QThread):
    log_signal = Signal(str)
    error_signal = Signal(str)
    status_signal = Signal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.observer = Observer()
        self.handler = ExcelHandler(self.check_excel_changes)
        self.running = True
        self.last_row_count = 0
        self.settings = QSettings('ExcelMonitor', 'Settings')
        self.log_file = None
        self.setup_logging()

    def setup_logging(self):
        """Setup log file if enabled in settings"""
        save_logs = self.settings.value('save_logs', False, type=bool)
        if save_logs:
            log_path = self.settings.value('log_file_path', '')
            if log_path:
                try:
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(log_path), exist_ok=True)
                    self.log_file = open(log_path, 'a', encoding='utf-8')
                    self.log_signal.emit(f"Logging to file: {log_path}")
                except Exception as e:
                    self.error_signal.emit(f"Error opening log file: {str(e)}")

    def write_to_log_file(self, message: str):
        """Write message to log file if enabled"""
        if self.log_file:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.log_file.write(f"[{timestamp}] {message}\n")
                self.log_file.flush()  # Ensure it's written to disk
            except Exception as e:
                self.error_signal.emit(f"Error writing to log file: {str(e)}")

    def run(self):
        self.observer.schedule(self.handler, os.path.dirname(self.file_path), recursive=False)
        self.observer.start()
        self.log_signal.emit(f"Started monitoring: {self.file_path}")
        self.write_to_log_file(f"Started monitoring: {self.file_path}")
        self.status_signal.emit("Monitoring")
        
        # Initial row count
        try:
            df = self.read_file(self.file_path)
            self.last_row_count = len(df)
            self.log_signal.emit(f"Initial row count: {self.last_row_count}")
            self.write_to_log_file(f"Initial row count: {self.last_row_count}")
        except Exception as e:
            self.error_signal.emit(f"Error reading initial file: {str(e)}")
            self.write_to_log_file(f"ERROR: Error reading initial file: {str(e)}")
            self.status_signal.emit("Error")

        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False
        self.observer.stop()
        self.observer.join()
        self.log_signal.emit("Stopped monitoring")
        self.write_to_log_file("Stopped monitoring")
        self.status_signal.emit("Stopped")
        
        # Close log file
        if self.log_file:
            self.log_file.close()
            self.log_file = None

    def read_file(self, file_path: str) -> pd.DataFrame:
        """Read different file formats and return a pandas DataFrame"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls', '.xlsm', '.xlsb']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def check_excel_changes(self, file_path: str):
        try:
            df = self.read_file(file_path)
            current_row_count = len(df)
            
            if current_row_count > self.last_row_count:
                new_rows = df.iloc[self.last_row_count:]
                self.log_signal.emit(f"Found {len(new_rows)} new rows:")
                self.write_to_log_file(f"Found {len(new_rows)} new rows:")
                
                # Log each new row with its content
                for idx, row in new_rows.iterrows():
                    row_data = row.to_dict()
                    formatted_data = ", ".join([f"{k}: {v}" for k, v in row_data.items()])
                    self.log_signal.emit(f"Row {idx + 1}: {formatted_data}")
                    self.write_to_log_file(f"Row {idx + 1}: {formatted_data}")
                
                self.sync_to_cloud(new_rows)
                self.last_row_count = current_row_count
        except Exception as e:
            self.error_signal.emit(f"Error processing file: {str(e)}")
            self.write_to_log_file(f"ERROR: Error processing file: {str(e)}")
            self.status_signal.emit("Error")

    def sync_to_cloud(self, new_rows: pd.DataFrame):
        try:
            api_url = self.settings.value('cloud_api_url')
            api_key = self.settings.value('cloud_api_key')
            
            if not api_url or not api_key:
                raise ValueError("Cloud API credentials not configured. Please set them in Settings.")

            # Convert DataFrame to JSON
            data = new_rows.to_dict(orient='records')
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            
            self.log_signal.emit(f"Successfully synced {len(data)} rows to cloud")
            self.write_to_log_file(f"Successfully synced {len(data)} rows to cloud")
        except Exception as e:
            self.error_signal.emit(f"Error syncing to cloud: {str(e)}")
            self.write_to_log_file(f"ERROR: Error syncing to cloud: {str(e)}")
            self.status_signal.emit("Error") 