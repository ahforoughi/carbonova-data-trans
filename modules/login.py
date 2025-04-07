from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QFont

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedWidth(300)
        self.setup_ui()
        self.load_password()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Enter Password")
        title.setFont(QFont('Arial', 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.verify_password)
        layout.addWidget(self.login_button)

        # Set enter key to trigger login
        self.password_input.returnPressed.connect(self.verify_password)

    def load_password(self):
        settings = QSettings('ExcelMonitor', 'Settings')
        self.stored_password = settings.value('app_password', '')
        
        # If no password is set, prompt to create one
        if not self.stored_password:
            self.set_new_password()

    def set_new_password(self):
        msg = QMessageBox()
        msg.setWindowTitle("Set Password")
        msg.setText("No password has been set. Would you like to set one now?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec() == QMessageBox.Yes:
            self.show_set_password_dialog()

    def show_set_password_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Password")
        dialog.setFixedWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        # Password input
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Enter new password")
        layout.addWidget(password_input)
        
        # Confirm password input
        confirm_input = QLineEdit()
        confirm_input.setEchoMode(QLineEdit.Password)
        confirm_input.setPlaceholderText("Confirm new password")
        layout.addWidget(confirm_input)
        
        # Save button
        save_button = QPushButton("Save")
        layout.addWidget(save_button)
        
        def save_password():
            if password_input.text() == confirm_input.text():
                if len(password_input.text()) >= 6:
                    settings = QSettings('ExcelMonitor', 'Settings')
                    settings.setValue('app_password', password_input.text())
                    dialog.accept()
                else:
                    QMessageBox.warning(dialog, "Error", "Password must be at least 6 characters long")
            else:
                QMessageBox.warning(dialog, "Error", "Passwords do not match")
        
        save_button.clicked.connect(save_password)
        password_input.returnPressed.connect(save_password)
        confirm_input.returnPressed.connect(save_password)
        
        dialog.exec()

    def verify_password(self):
        if self.password_input.text() == self.stored_password:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Incorrect password")
            self.password_input.clear() 