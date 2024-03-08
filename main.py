import os
import logparser
import time
import threading
import configparser

def get_chat_log_path_from_settings():
    settings_file_path = "settings.ini"

    if os.path.exists(settings_file_path):
        config = configparser.ConfigParser()
        config.read(settings_file_path)

        if "LOGFILE" in config["DEFAULT"]:
            return config["DEFAULT"]["LOGFILE"]
        else:
            print("Error: settings.ini not found.")

        return None

def main():
    chat_log_file_path = get_chat_log_path_from_settings()

    # Create a thread for logparser.py
    log_parser_thread = threading.Thread(target=logparser.start_monitoring, args=(chat_log_file_path,))
    log_parser_thread.start()

    try:
        # Main app logic
        time.sleep(1)
    except KeyboardInterrupt:
        # Stop the log parser when main program is interrupted
        log_parser_thread.join()

if __name__ == "__main__":
    main()
