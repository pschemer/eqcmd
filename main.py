import os
import logparser
import time
import threading

def get_chat_log_path():
    return 'E:\EQ\EQ-Test\Logs\eqlog_Fatguylilcoat_test.txt'
    '''
    while True:
        chat_log_path = input("Enter the path to the chat log file: ")
        if os.path.exists(chat_log_path):
            return chat_log_path
        else:
            print("Invalid path. Please enter a valid path.")
    '''

def main():
    chat_log_file_path = get_chat_log_path()

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
