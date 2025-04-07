import os
from datetime import datetime
from typing import Optional

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QTextEdit, QFileDialog, QLabel, QHBoxLayout, QFrame, 
                            QStyle, QStyleFactory, QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor

from modules.monitor import ExcelMonitor
from modules.settings import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Monitor")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set the application style
        self.setStyle(QStyleFactory.create('Fusion'))
        
        # Set dark theme
        self.set_dark_theme()
        
        self.monitor: Optional[ExcelMonitor] = None
        self.setup_ui()

    def set_dark_theme(self):
        """Set a dark theme for the application"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_layout = QHBoxLayout(header_frame)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setFont(QFont('Arial', 10))
        header_layout.addWidget(self.file_label)
        
        self.status_label = QLabel("Status: Not Monitoring")
        self.status_label.setFont(QFont('Arial', 10))
        header_layout.addWidget(self.status_label)
        
        main_layout.addWidget(header_frame)

        # Buttons
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        select_button = QPushButton("Select File")
        select_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        select_button.clicked.connect(self.select_file)
        select_button.setMinimumHeight(40)
        button_layout.addWidget(select_button)
        
        settings_button = QPushButton("Settings")
        settings_button.setIcon(self.style().standardIcon(QStyle.SP_DialogHelpButton))
        settings_button.clicked.connect(self.show_settings)
        settings_button.setMinimumHeight(40)
        button_layout.addWidget(settings_button)
        
        main_layout.addWidget(button_frame)

        # Log display
        log_frame = QFrame()
        log_frame.setFrameStyle(QFrame.StyledPanel)
        log_layout = QVBoxLayout(log_frame)
        
        log_header = QLabel("Activity Log")
        log_header.setFont(QFont('Arial', 12, QFont.Bold))
        log_layout.addWidget(log_header)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont('Consolas', 10))
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
            }
        """)
        log_layout.addWidget(self.log_display)
        
        main_layout.addWidget(log_frame)

    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.log_message("Settings updated successfully")
            
            # If monitor is running, restart it to apply new settings
            if self.monitor:
                current_file = self.monitor.file_path
                self.monitor.stop()
                self.monitor = ExcelMonitor(current_file)
                self.monitor.log_signal.connect(self.log_message)
                self.monitor.error_signal.connect(self.log_error)
                self.monitor.status_signal.connect(self.update_status)
                self.monitor.start()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Supported Files (*.xlsx *.xls *.csv *.xlsm *.xlsb);;Excel Files (*.xlsx *.xls *.xlsm *.xlsb);;CSV Files (*.csv);;All Files (*.*)"
        )
        
        if file_path:
            self.file_label.setText(f"Monitoring: {os.path.basename(file_path)}")
            if self.monitor:
                self.monitor.stop()
            
            self.monitor = ExcelMonitor(file_path)
            self.monitor.log_signal.connect(self.log_message)
            self.monitor.error_signal.connect(self.log_error)
            self.monitor.status_signal.connect(self.update_status)
            self.monitor.start()

    def log_message(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.append(f'<span style="color: #4CAF50;">[{timestamp}]</span> {message}')

    def log_error(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.append(f'<span style="color: #FF5252;">[{timestamp}] ERROR:</span> {message}')

    def update_status(self, status: str):
        self.status_label.setText(f"Status: {status}")

    def closeEvent(self, event):
        if self.monitor:
            self.monitor.stop()
        event.accept() 