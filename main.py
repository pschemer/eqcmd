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

def addEvent(args):
    logparser.event_functions[args[0]] = args[1]
    print(f"add event '{args}'")

def delEvent(args):
    if args[0] in logparser.event_functions.keys():
        del(logparser.event_functions[args[0]])
    print(f"del event '{args}'")

def printEvents(args):
    for event in logparser.event_functions.items():
        print(event)

menuItems = {
    "add":addEvent,
    "del":delEvent,
    "print":printEvents,
}

def printmenu():
    print(f"Menu Items:")
    for item in menuItems.keys():
        print(item)

def main():
    chat_log_file_path = get_chat_log_path_from_settings()

    # Create a thread for logparser.py
    log_parser_thread = threading.Thread(target=logparser.start_monitoring, args=(chat_log_file_path,))
    log_parser_thread.start()

    try:
        # Main app logic
        while True:
            printmenu()
            command = []
            user_input = input(": ").strip()
            if user_input.lower() == 'done':
                log_parser_thread.join()
                print("Parser stopped")
                break
            command.append(user_input)
            if command[0] in menuItems.keys():
                menuItems[command[0]](command[1:])
        exit
        
    except KeyboardInterrupt:
        # Stop the log parser when main program is interrupted
        log_parser_thread.join()
        print("Parser stopped")

if __name__ == "__main__":
    main()
