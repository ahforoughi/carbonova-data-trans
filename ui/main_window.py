from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        # Create central widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create main layout
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Create status label
        self.status_label = QLabel(self.centralwidget)
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.status_label)
        
        # Create buttons layout
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        
        # Create select file button
        self.select_file_button = QPushButton(self.centralwidget)
        self.select_file_button.setObjectName("select_file_button")
        self.select_file_button.setText("Select Excel File")
        self.buttons_layout.addWidget(self.select_file_button)
        
        # Create settings button
        self.settings_button = QPushButton(self.centralwidget)
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setText("Settings")
        self.buttons_layout.addWidget(self.settings_button)
        
        self.verticalLayout.addLayout(self.buttons_layout)
        
        # Create log text area
        self.log_text = QTextEdit(self.centralwidget)
        self.log_text.setObjectName("log_text")
        self.log_text.setReadOnly(True)
        self.verticalLayout.addWidget(self.log_text)
        
        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Set window title
        MainWindow.setWindowTitle("Excel Monitor") 