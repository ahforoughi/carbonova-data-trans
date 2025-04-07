import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QTextEdit, QFileDialog, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.last_modified = 0
        self.last_row_count = 0

    def on_modified(self, event):
        if event.src_path.endswith('.xlsx'):
            current_time = time.time()
            if current_time - self.last_modified > 1:  # Debounce for 1 second
                self.last_modified = current_time
                self.callback(event.src_path)

class ExcelMonitor(QThread):
    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.observer = Observer()
        self.handler = ExcelHandler(self.check_excel_changes)
        self.running = True
        self.last_row_count = 0

    def run(self):
        self.observer.schedule(self.handler, os.path.dirname(self.file_path), recursive=False)
        self.observer.start()
        self.log_signal.emit(f"Started monitoring: {self.file_path}")
        
        # Initial row count
        try:
            df = pd.read_excel(self.file_path)
            self.last_row_count = len(df)
            self.log_signal.emit(f"Initial row count: {self.last_row_count}")
        except Exception as e:
            self.error_signal.emit(f"Error reading initial file: {str(e)}")

        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False
        self.observer.stop()
        self.observer.join()
        self.log_signal.emit("Stopped monitoring")

    def check_excel_changes(self, file_path: str):
        try:
            df = pd.read_excel(file_path)
            current_row_count = len(df)
            
            if current_row_count > self.last_row_count:
                new_rows = df.iloc[self.last_row_count:]
                self.sync_to_cloud(new_rows)
                self.last_row_count = current_row_count
                self.log_signal.emit(f"Found {len(new_rows)} new rows")
        except Exception as e:
            self.error_signal.emit(f"Error processing file: {str(e)}")

    def sync_to_cloud(self, new_rows: pd.DataFrame):
        try:
            api_url = os.getenv('CLOUD_API_URL')
            api_key = os.getenv('CLOUD_API_KEY')
            
            if not api_url or not api_key:
                raise ValueError("Cloud API credentials not found in .env file")

            # Convert DataFrame to JSON
            data = new_rows.to_dict(orient='records')
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            
            self.log_signal.emit(f"Successfully synced {len(data)} rows to cloud")
        except Exception as e:
            self.error_signal.emit(f"Error syncing to cloud: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel File Monitor")
        self.setGeometry(100, 100, 800, 600)
        
        self.monitor: Optional[ExcelMonitor] = None
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # File selection
        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        select_button = QPushButton("Select Excel File")
        select_button.clicked.connect(self.select_file)
        layout.addWidget(select_button)

        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            self.file_label.setText(f"Monitoring: {file_path}")
            if self.monitor:
                self.monitor.stop()
            
            self.monitor = ExcelMonitor(file_path)
            self.monitor.log_signal.connect(self.log_message)
            self.monitor.error_signal.connect(self.log_error)
            self.monitor.start()

    def log_message(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")

    def log_error(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.append(f"[{timestamp}] ERROR: {message}")

    def closeEvent(self, event):
        if self.monitor:
            self.monitor.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 