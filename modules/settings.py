import os
from PySide6.QtWidgets import (QDialog, QLineEdit, QFormLayout, QPushButton, 
                            QHBoxLayout, QFileDialog, QCheckBox, QVBoxLayout, QLabel)
from PySide6.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("ExcelMonitor", "Settings")
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # API Settings
        api_layout = QVBoxLayout()
        api_layout.addWidget(QLabel("API Settings"))
        
        # API URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("API URL:"))
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setText(self.settings.value("api_url", ""))
        url_layout.addWidget(self.api_url_edit)
        api_layout.addLayout(url_layout)
        
        # API Key
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("API Key:"))
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setText(self.settings.value("api_key", ""))
        key_layout.addWidget(self.api_key_edit)
        api_layout.addLayout(key_layout)
        
        layout.addLayout(api_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_settings(self):
        # Save API settings
        self.settings.setValue("api_url", self.api_url_edit.text())
        self.settings.setValue("api_key", self.api_key_edit.text())
        
        self.accept() 