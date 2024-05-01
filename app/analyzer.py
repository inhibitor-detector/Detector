import sys
import os
import watchdog

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, logs_file):
        self.logs_file = logs_file
        self.last_line_number = 0
        self.is_running = True

    def on_modified(self, event):

        with open(self.logs_file, 'r') as file:
            new_lines = file.readlines()[self.last_line_number:]  # Read from last read, up to the end
            for line in new_lines:
                # Perform simple analysis on each line
                if "ffffff" in line:
                    print("Inhibitor detected")
                    # curl xxx
                    # TODO make a post here with requests or something cheto
                elif "exit()" in line:  # exit manually by dev or automatically when rfcat finishes
                    print("Exit detected")
                    self.is_running = False

                self.last_line_number += 1


def main():
    print("HELLO, I AM ANALYZER")

    # Check if the logs file argument is provided
    if len(sys.argv)!= 2:
        print(f"Usage: {sys.argv[0]} <logs_file>")
        sys.exit(1)

    # Get the logs file from the command-line argument
    logs_file = sys.argv[1]

    if not os.path.isfile(logs_file):
        print(f"Error: The logs file '{logs_file}' does not exist.")
        sys.exit(1)

    event_handler = LogFileHandler(logs_file)

    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(logs_file), recursive=False)
    observer.start()

    try:
        while event_handler.is_running:
            time.sleep(1)
        observer.stop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
