'''
This script uses watchdog to monitor file modifications efficiently. 
The ChatLogHandler class extends FileSystemEventHandler and overrides the on_modified method to process file modifications. 
The observer is then set up to watch for modifications in the specified path.

Make sure to adjust the chat_log_file_path and the paths in the observer accordingly based on your actual file locations.
'''
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import keyboard
import sendkeys

def send_keystrokes(window_title, keystrokes):
    sendkeys.KeyPress(window_title, keystrokes)   

def helloPat(text):
    send_keystrokes('EverQuest', '1')

def goodbyeSam(text):
    send_keystrokes('EverQuest', '2')

event_functions = {
    "Hello Pat!": helloPat,
    "Goodbye Sam!": goodbyeSam,
    # Add more events and corresponding functions as needed
}

class ChatLogHandler(FileSystemEventHandler):
    def __init__(self, chat_log_file_path):
        super().__init__()
        self.chat_log_file_path = chat_log_file_path
        self.last_position = os.path.getsize(chat_log_file_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        with open(self.chat_log_file_path, 'r') as file:
            file.seek(self.last_position)
            new_entries = file.readlines()
            if new_entries:
                for entry in new_entries:
                    entry.strip()
                    for event_text, function in event_functions.items():
                        if event_text in entry:
                            print(f"event '{event_text}' found in new entry")
                            function(entry)
                # Update the last processed position
                self.last_position = file.tell()

def start_monitoring(chat_log_file_path):
    print(f"Trying to monitor '{chat_log_file_path}'")
    event_handler = ChatLogHandler(chat_log_file_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(chat_log_file_path), recursive=False)
    observer.start()
    print(f"Starting monitoring on '{chat_log_file_path}'")
    send_keystrokes('EverQuest', 'h')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
