'''
This script uses watchdog to monitor file modifications efficiently. 
The ChatLogHandler class extends FileSystemEventHandler and overrides the on_modified method to process file modifications. 
The observer is then set up to watch for modifications in the specified path.

Make sure to adjust the chat_log_file_path and the paths in the observer accordingly based on your actual file locations.
'''

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import keyboard

# Function to send keystrokes to a specific window title
def send_keystrokes(window_title, keystrokes):
    # Implement the logic to send keystrokes to the specified window
    print(f"Sending keystrokes '{keystrokes}' to window '{window_title}'")

# Function for the event "Hello Pat!"
def helloPat():
    send_keystrokes('MyChat', '1')

# Function for the event "Goodbye Sam!"
def goodbyeSam():
    send_keystrokes('MyChat', '2')

# Dictionary mapping chat log events to corresponding functions
event_functions = {
    "Hello Pat!": helloPat,
    "Goodbye Sam!": goodbyeSam,
    # Add more events and corresponding functions as needed
}

# Path to the chat log file
chat_log_file_path = 'path/to/your/chat_log.txt'

# Custom event handler to process file system events
class ChatLogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        with open(chat_log_file_path, 'r') as file:
            new_entries = file.readlines()
            if new_entries:
                for entry in new_entries:
                    for event_text, function in event_functions.items():
                        if event_text in entry:
                            function()

# Set up the file system event handler
event_handler = ChatLogHandler()

# Set up the observer to watch for file modifications
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
