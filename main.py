import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtGui import QIcon
from modules.monitor import ExcelMonitor
from modules.settings import SettingsDialog
from modules.file_handler import ExcelHandler
from modules.logger import Logger
from ui.main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Force light mode
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
        """)
        
        # Set window icon
        self.setWindowIcon(QIcon("app_icon.ico"))
        
        # Initialize components
        self.settings = QSettings("ExcelMonitor", "Settings")
        self.logger = Logger()
        self.monitor = None
        self.file_handler = None
        
        # Connect signals
        self.ui.select_file_button.clicked.connect(self.select_file)
        self.ui.settings_button.clicked.connect(self.show_settings)
        
        # Set initial state
        self.update_status("Ready")
        self.log_message("Application started")
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls *.csv *.xlsm *.xlsb)"
        )
        
        if file_path:
            self.start_monitoring(file_path)
    
    def start_monitoring(self, file_path):
        if self.monitor:
            self.monitor.stop()
        
        self.monitor = ExcelMonitor(file_path)
        self.monitor.log_signal.connect(self.log_message)
        self.monitor.status_signal.connect(self.update_status)
        self.monitor.start()
        
        self.file_handler = ExcelHandler(self.monitor.check_excel_changes)
        self.file_handler.start_watching(file_path)
        
        self.log_message(f"Started monitoring: {file_path}")
        self.update_status("Monitoring")
    
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == SettingsDialog.Accepted:
            self.log_message("Settings updated")
    
    def log_message(self, message):
        self.ui.log_text.append(message)
        self.logger.log(message)
    
    def update_status(self, status):
        self.ui.status_label.setText(f"Status: {status}")
    
    def closeEvent(self, event):
        if self.monitor:
            self.monitor.stop()
        if self.file_handler:
            self.file_handler.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Force light mode for the entire application
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QApplication {
            background-color: #ffffff;
            color: #000000;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 