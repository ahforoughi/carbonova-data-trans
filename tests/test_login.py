import unittest
import os
import tempfile
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QSettings
from modules.login import LoginDialog

# Create a QApplication instance for testing
app = QApplication([])

class TestLoginDialog(unittest.TestCase):
    def setUp(self):
        # Create a settings dialog
        self.dialog = LoginDialog()
        
        # Clear settings
        settings = QSettings('ExcelMonitor', 'Settings')
        settings.clear()
    
    def tearDown(self):
        # Clear settings
        settings = QSettings('ExcelMonitor', 'Settings')
        settings.clear()
    
    def test_load_password_empty(self):
        # Load password
        self.dialog.load_password()
        
        # Check if stored_password is empty
        self.assertEqual(self.dialog.stored_password, '')
    
    def test_load_password_existing(self):
        # Set password
        settings = QSettings('ExcelMonitor', 'Settings')
        settings.setValue('app_password', 'test_password')
        
        # Load password
        self.dialog.load_password()
        
        # Check if stored_password is set correctly
        self.assertEqual(self.dialog.stored_password, 'test_password')
    
    @patch('PySide6.QtWidgets.QMessageBox.exec')
    def test_set_new_password_yes(self, mock_exec):
        # Mock message box to return Yes
        mock_exec.return_value = QMessageBox.Yes
        
        # Mock show_set_password_dialog
        self.dialog.show_set_password_dialog = MagicMock()
        
        # Call set_new_password
        self.dialog.set_new_password()
        
        # Check if show_set_password_dialog was called
        self.dialog.show_set_password_dialog.assert_called_once()
    
    @patch('PySide6.QtWidgets.QMessageBox.exec')
    def test_set_new_password_no(self, mock_exec):
        # Mock message box to return No
        mock_exec.return_value = QMessageBox.No
        
        # Mock show_set_password_dialog
        self.dialog.show_set_password_dialog = MagicMock()
        
        # Call set_new_password
        self.dialog.set_new_password()
        
        # Check if show_set_password_dialog was not called
        self.dialog.show_set_password_dialog.assert_not_called()
    
    @patch('PySide6.QtWidgets.QMessageBox.warning')
    def test_verify_password_correct(self, mock_warning):
        # Set stored password
        self.dialog.stored_password = 'test_password'
        
        # Set password input
        self.dialog.password_input.setText('test_password')
        
        # Mock accept
        self.dialog.accept = MagicMock()
        
        # Call verify_password
        self.dialog.verify_password()
        
        # Check if accept was called
        self.dialog.accept.assert_called_once()
        
        # Check if warning was not called
        mock_warning.assert_not_called()
    
    @patch('PySide6.QtWidgets.QMessageBox.warning')
    def test_verify_password_incorrect(self, mock_warning):
        # Set stored password
        self.dialog.stored_password = 'test_password'
        
        # Set password input
        self.dialog.password_input.setText('wrong_password')
        
        # Mock accept
        self.dialog.accept = MagicMock()
        
        # Call verify_password
        self.dialog.verify_password()
        
        # Check if accept was not called
        self.dialog.accept.assert_not_called()
        
        # Check if warning was called
        mock_warning.assert_called_once()
        
        # Check if password input was cleared
        self.assertEqual(self.dialog.password_input.text(), '')

if __name__ == '__main__':
    unittest.main() 