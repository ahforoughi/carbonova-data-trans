import os
from PySide6.QtWidgets import (QDialog, QLineEdit, QFormLayout, QPushButton, 
                            QHBoxLayout, QFileDialog, QCheckBox)
from PySide6.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Cloud API URL
        self.api_url_input = QLineEdit()
        self.api_url_input.setPlaceholderText("https://api.example.com/data")
        layout.addRow("Cloud API URL:", self.api_url_input)
        
        # Cloud API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your API key")
        layout.addRow("Cloud API Key:", self.api_key_input)
        
        # Log settings
        self.save_logs_checkbox = QCheckBox("Save logs to file")
        layout.addRow("", self.save_logs_checkbox)
        
        self.log_path_input = QLineEdit()
        self.log_path_input.setPlaceholderText("Path to log file")
        layout.addRow("Log file path:", self.log_path_input)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_log_path)
        layout.addRow("", browse_button)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow("", button_layout)

    def browse_log_path(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Log File",
            "",
            "Log Files (*.log);;Text Files (*.txt);;All Files (*.*)"
        )
        if file_path:
            self.log_path_input.setText(file_path)

    def load_settings(self):
        settings = QSettings('ExcelMonitor', 'Settings')
        self.api_url_input.setText(settings.value('cloud_api_url', ''))
        self.api_key_input.setText(settings.value('cloud_api_key', ''))
        self.save_logs_checkbox.setChecked(settings.value('save_logs', False, type=bool))
        self.log_path_input.setText(settings.value('log_file_path', ''))

    def save_settings(self):
        settings = QSettings('ExcelMonitor', 'Settings')
        settings.setValue('cloud_api_url', self.api_url_input.text())
        settings.setValue('cloud_api_key', self.api_key_input.text())
        settings.setValue('save_logs', self.save_logs_checkbox.isChecked())
        settings.setValue('log_file_path', self.log_path_input.text())
        self.accept() 