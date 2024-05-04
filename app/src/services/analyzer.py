import sys
import os
import requests
import time

class AnalyzerService:
    def __init__(self, logs_file):
        print("Initializing Analyzer service...")

        if not os.path.isfile(logs_file):
            print(f"Error: The logs file '{logs_file}' does not exist.")
            sys.exit(1)

        self.logs_file = logs_file
        self.last_modified = os.path.getmtime(self.logs_file)
        self.last_line_number = 0

        print("Analyzer service initialized.")

    def analyze(self):
        last_modified = os.path.getmtime(self.logs_file)
        if last_modified > self.last_modified:
            self.last_modified = last_modified
            self.run_analysis()

    
    def run_analysis(self):
        print("Running Analyzer service...")
        with open(self.logs_file, 'r') as file:
            new_lines = file.readlines()[self.last_line_number:]  # Read from last read, up to the end
            for line in new_lines:
                # Perform simple analysis on each line
                if "ffffffffff" in line:
                    print("Inhibitor detected")
                    # curl xxx
                    # TODO make a post here with requests or something cheto
                    response = requests.get("http://wttr.in")
                    print(response)
                # TODO remove on prod:
                elif "exit()" in line:  # exit manually by dev or automatically when rfcat finishes
                    print("Exit detected")
                    self.is_running = False

                self.last_line_number += 1 #update read position



# class LogFileHandler(FileSystemEventHandler):
#     def __init__(self, logs_file):
#         # self.logs_file = logs_file
#         # self.last_line_number = 0
#         # self.is_running = True

#     def on_modified(self, event):
        # with open(self.logs_file, 'r') as file:
        #     new_lines = file.readlines()[self.last_line_number:]  # Read from last read, up to the end
        #     for line in new_lines:
        #         # Perform simple analysis on each line
        #         if "ffffff" in line:
        #             print("Inhibitor detected")
        #             # curl xxx
        #             # TODO make a post here with requests or something cheto
        #             response = requests.get("http://wttr.in")
        #             print(response)
        #         elif "exit()" in line:  # exit manually by dev or automatically when rfcat finishes
        #             print("Exit detected")
        #             self.is_running = False

        #         self.last_line_number += 1