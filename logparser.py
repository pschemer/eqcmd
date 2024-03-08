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
import pyautogui
import pygetwindow as gw

def send_keystrokes(window_title, keystrokes):
    print(f"Sending keystrokes '{keystrokes}' to window '{window_title}'")

    # Implement the logic to send keystrokes to the specified window
    try:
        # Get the window handle based on the window title
        window = gw.getWindowsWithTitle(window_title)[0]

        # Activate the window
        window.activate()

        # Send keystrokes
        pyautogui.write(keystrokes)
    except Exception as e:
        print(f"Error sending keystrokes to window '{window_title}': {e}")

def helloPat():
    send_keystrokes('EverQuest', '1')

def goodbyeSam():
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

    def on_modified(self, event):
        print("Modification detected")
        if event.is_directory:
            return
        with open(self.chat_log_file_path, 'r') as file:
            new_entries = file.readlines()
            if new_entries:
                print("New entries...")
                for entry in new_entries:
                    for event_text, function in event_functions.items():
                        if event_text in entry:
                            print(f"event '{event_text}' found in new entry")
                            function()

def start_monitoring(chat_log_file_path):
    print(f"Trying to monitor '{chat_log_file_path}'")
    event_handler = ChatLogHandler(chat_log_file_path)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    print(f"Starting monitoring on '{chat_log_file_path}'")
    send_keystrokes('EverQuest', 'h')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
