import unittest
import os
import tempfile
import pandas as pd
from unittest.mock import MagicMock, patch
from modules.monitor import ExcelMonitor

class TestExcelMonitor(unittest.TestCase):
    def setUp(self):
        # Create a temporary Excel file
        self.temp_dir = tempfile.mkdtemp()
        self.excel_file = os.path.join(self.temp_dir, "test.xlsx")
        
        # Create initial test data
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        self.df.to_excel(self.excel_file, index=False)
        
        # Create monitor with mock signals
        self.monitor = ExcelMonitor(self.excel_file)
        self.monitor.log_signal = MagicMock()
        self.monitor.status_signal = MagicMock()
    
    def tearDown(self):
        # Clean up
        if os.path.exists(self.excel_file):
            os.remove(self.excel_file)
        os.rmdir(self.temp_dir)
    
    def test_read_excel_file(self):
        # Test reading Excel file
        df = self.monitor.read_file(self.excel_file)
        self.assertEqual(len(df), 3)
        self.assertEqual(df.iloc[0]['A'], 1)
        self.assertEqual(df.iloc[0]['B'], 'a')
    
    @patch('modules.monitor.requests.post')
    def test_sync_to_cloud(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response
        
        # Test syncing
        result = self.monitor.sync_to_cloud([{"A": 4, "B": "d"}])
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    def test_detect_changes(self):
        # Add a new row
        new_df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': ['a', 'b', 'c', 'd']
        })
        new_df.to_excel(self.excel_file, index=False)
        
        # Set initial row count
        self.monitor.last_row_count = 3
        
        # Test change detection
        self.monitor.check_excel_changes(self.excel_file)
        
        # Verify signals were emitted
        self.monitor.log_signal.emit.assert_called()
        self.monitor.status_signal.emit.assert_called()

if __name__ == '__main__':
    unittest.main() 