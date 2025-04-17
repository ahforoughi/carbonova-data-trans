import unittest
import os
import tempfile
import pandas as pd
from unittest.mock import MagicMock
from modules.file_handler import ExcelHandler

class TestExcelHandler(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and Excel file
        self.temp_dir = tempfile.mkdtemp()
        self.excel_file = os.path.join(self.temp_dir, "test.xlsx")
        
        # Create initial test data
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        self.df.to_excel(self.excel_file, index=False)
        
        # Create handler with mock callback
        self.callback = MagicMock()
        self.handler = ExcelHandler(self.callback)
        self.handler.last_row_count = len(self.df)
    
    def tearDown(self):
        # Clean up
        if os.path.exists(self.excel_file):
            os.remove(self.excel_file)
        os.rmdir(self.temp_dir)
    
    def test_detect_new_rows(self):
        # Add a new row
        new_df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': ['a', 'b', 'c', 'd']
        })
        new_df.to_excel(self.excel_file, index=False)
        
        # Create mock event
        event = MagicMock()
        event.src_path = self.excel_file
        
        # Test detection
        self.handler.on_modified(event)
        
        # Verify callback was called with new row
        self.callback.assert_called_once()
        new_rows = self.callback.call_args[0][0]
        self.assertEqual(len(new_rows), 1)
        self.assertEqual(new_rows[0]['A'], 4)
        self.assertEqual(new_rows[0]['B'], 'd')
    
    def test_no_changes(self):
        # Create mock event
        event = MagicMock()
        event.src_path = self.excel_file
        
        # Test no changes
        self.handler.on_modified(event)
        
        # Verify callback was not called
        self.callback.assert_not_called()

if __name__ == '__main__':
    unittest.main() 