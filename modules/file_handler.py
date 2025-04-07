import time
from watchdog.events import FileSystemEventHandler

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.last_modified = 0
        self.last_row_count = 0

    def on_modified(self, event):
        if event.src_path.endswith(('.xlsx', '.xls', '.csv', '.xlsm', '.xlsb')):
            current_time = time.time()
            if current_time - self.last_modified > 1:  # Debounce for 1 second
                self.last_modified = current_time
                self.callback(event.src_path) 