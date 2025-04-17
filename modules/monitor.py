import os
import time
import uuid
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
        self.file_id = str(uuid.uuid4())[:16]
        print(f"[DEBUG] Monitor initialized for file: {file_path}")
        print(f"[DEBUG] Generated file ID: {self.file_id}")
        self.upload_file()

    def run(self):
        print("[DEBUG] Starting monitor thread")
        self.observer.schedule(self.handler, os.path.dirname(self.file_path), recursive=False)
        self.observer.start()
        self.log_signal.emit("Monitor started")
        self.status_signal.emit("Monitoring")
        
        try:
            df = self.read_file(self.file_path)
            self.last_row_count = len(df)
            print(f"[DEBUG] Initial row count: {self.last_row_count}")
            self.log_signal.emit(f"Initial rows: {self.last_row_count}")
        except Exception as e:
            print(f"[DEBUG] Error reading file: {str(e)}")
            self.error_signal.emit(f"Error reading file: {str(e)}")
            self.status_signal.emit("Error")

        while self.running:
            time.sleep(1)

    def stop(self):
        print("[DEBUG] Stopping monitor")
        self.running = False
        self.observer.stop()
        self.observer.join()
        self.log_signal.emit("Monitor stopped")
        self.status_signal.emit("Stopped")

    def read_file(self, file_path: str) -> pd.DataFrame:
        print(f"[DEBUG] Reading file: {file_path}")
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls', '.xlsm', '.xlsb']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def check_excel_changes(self, file_path: str):
        try:
            print(f"[DEBUG] Checking for changes in: {file_path}")
            df = self.read_file(file_path)
            current_row_count = len(df)
            
            if current_row_count > self.last_row_count:
                new_rows = df.iloc[self.last_row_count:]
                print(f"[DEBUG] Found {len(new_rows)} new rows")
                self.log_signal.emit(f"New rows detected: {len(new_rows)}")
                
                for idx, row in new_rows.iterrows():
                    row_data = row.to_dict()
                    print(f"[DEBUG] New row {idx + 1}: {row_data}")
                    self.log_signal.emit(f"Row {idx + 1}: {row_data}")
                
                self.sync_to_cloud(new_rows)
                self.last_row_count = current_row_count
        except Exception as e:
            print(f"[DEBUG] Error processing changes: {str(e)}")
            self.error_signal.emit(f"Error processing changes: {str(e)}")
            self.status_signal.emit("Error")

    def upload_file(self):
        try:
            api_url = self.settings.value('api_url')
            api_key = self.settings.value('api_key')
            
            print(f"[DEBUG] API URL: {api_url}")
            print(f"[DEBUG] API Key: {api_key}")
            
            if not api_url or not api_key:
                print("[DEBUG] API credentials not set")
                self.error_signal.emit("API credentials not set")
                return

            print("[DEBUG] Starting file upload")
            self.log_signal.emit("Uploading file...")
            
            with open(self.file_path, 'rb') as file:
                file_content = file.read()

            # Get file extension and type
            file_ext = os.path.splitext(self.file_path)[1].lower()
            file_type = 'csv' if file_ext == '.csv' else 'excel'
            
            # Prepare the request
            files = {
                'file': (os.path.basename(self.file_path), file_content)
            }
            data = {
                'file_id': self.file_id
            }
            
            # Set proper headers for multipart form data
            headers = {
                'Authorization': f'Token {api_key}',
                'original_filename': os.path.basename(self.file_path),
                'file_type': file_type
            }
            
            print(f"[DEBUG] Uploading to: {api_url}/api/file-management/files/")
            print(f"[DEBUG] Headers: {headers}")
            print(f"[DEBUG] File ID: {self.file_id}")
            print(f"[DEBUG] File type: {file_type}")
            
            # Make the request
            response = requests.post(
                f"{api_url}/api/file-management/files/",
                data=data,
                files=files,
                headers=headers
            )
            
            # Log response details
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response headers: {response.headers}")
            print(f"[DEBUG] Response content: {response.text}")
            
            # Check for specific error cases
            if response.status_code == 401:
                print("[DEBUG] Authentication failed. Check API key.")
                self.error_signal.emit("Authentication failed. Please check your API key.")
                return
            elif response.status_code == 400:
                print("[DEBUG] Bad request. Check request format.")
                self.error_signal.emit(f"Bad request: {response.text}")
                return
            
            response.raise_for_status()
            
            print(f"[DEBUG] File uploaded successfully. ID: {self.file_id}")
            self.log_signal.emit(f"File uploaded successfully. ID: {self.file_id}")
        except requests.exceptions.RequestException as e:
            print(f"[DEBUG] Request error: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"[DEBUG] Error response: {e.response.text}")
            self.error_signal.emit(f"Upload failed: {str(e)}")
            self.status_signal.emit("Error")
        except Exception as e:
            print(f"[DEBUG] Unexpected error: {str(e)}")
            self.error_signal.emit(f"Upload failed: {str(e)}")
            self.status_signal.emit("Error")

    def sync_to_cloud(self, new_rows: pd.DataFrame):
        try:
            api_url = self.settings.value('api_url')
            api_key = self.settings.value('api_key')
            
            if not api_url or not api_key:
                print("[DEBUG] API credentials not set")
                self.error_signal.emit("API credentials not set")
                return

            print(f"[DEBUG] Starting sync of {len(new_rows)} rows")
            self.log_signal.emit(f"Syncing {len(new_rows)} rows...")
            
            for idx, (_, row) in enumerate(new_rows.iterrows(), 1):
                update_data = row.to_dict()
                payload = {
                    "file_id": self.file_id,
                    "update_data": update_data
                }
                
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                
                print(f"[DEBUG] Updating row {idx}: {update_data}")
                self.log_signal.emit(f"Updating row {idx}: {update_data}")
                
                response = requests.post(f"{api_url}/api/file-management/files/update_rows/", 
                                      json=payload, 
                                      headers=headers)
                response.raise_for_status()
                
                print(f"[DEBUG] Row {idx} updated successfully")
                self.log_signal.emit(f"Row {idx} updated successfully")
            
            print("[DEBUG] All rows synced successfully")
            self.log_signal.emit("All rows synced successfully")
        except Exception as e:
            print(f"[DEBUG] Sync failed: {str(e)}")
            self.error_signal.emit(f"Sync failed: {str(e)}")
            self.status_signal.emit("Error") 