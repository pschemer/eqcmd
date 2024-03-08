import logparser  # Assuming logparser.py is in the same directory

def get_chat_log_path():
    while True:
        chat_log_path = input("Enter the path to the chat log file: ")
        if os.path.exists(chat_log_path):
            return chat_log_path
        else:
            print("Invalid path. Please enter a valid path.")

def main():
    chat_log_file_path = get_chat_log_path()

    try:
        logparser.start_monitoring(chat_log_file_path)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()