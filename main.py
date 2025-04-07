import sys
from PySide6.QtWidgets import QApplication
from modules.ui import MainWindow
from modules.login import LoginDialog

def main():
    app = QApplication(sys.argv)
    
    # Show login dialog first
    login_dialog = LoginDialog()
    if login_dialog.exec() == LoginDialog.Accepted:
        # Only show main window if login was successful
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 