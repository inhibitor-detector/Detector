import os
import time
import threading

class AnalyzerService:
    def __init__(self, detector, logs_file):
        print("Initializing Analyzer service...")
        self.detector = detector
        self.logs_file = logs_file
        self.last_modified_time = os.path.getmtime(self.logs_file)
        self.last_line_number_read = 0
        self.inhibiton_detected = False
        self.rfcat_has_exited = False
        self.logs_lock = threading.Lock()
        print("Analyzer service initialized.")

    def run(self):
        print("Running Analyzer service...")
        while True:
            self.check_logs()
            time.sleep(3)
    
    def check_logs(self):
        with self.logs_lock:
            last_modified_time = os.path.getmtime(self.logs_file)
            if last_modified_time > self.last_modified_time:
                print("Logs file modified, running analysis...")
                self.last_modified_time = last_modified_time
                self.run_analysis()
    
    def run_analysis(self):
        print("Running analysis of log file...")
        with open(self.logs_file, 'r') as file:
            #read from last line read, up to the max of the file at this moment.
            new_lines = file.readlines()[self.last_line_number_read:]
            #then close the file so there is no stuck-reading problems.
        for line in new_lines:
            if not self.inhibiton_detected:
                if "ffffffffff" in line:
                    print("Inhibitor detected by Analyzer")
                    self.inhibiton_detected = True
                    self.send_inhibition_detected()
                    #i want to run the post on another thread so i can continue reading the file

                elif "Error" in line:
                    print("Error detected:")
                    if "Access denied (insufficient permissions)" in line:
                        print("Access denied:")
                        print("\tDid you run with sudo?")

                    elif "No Dongle Found" in line:
                        print("No Dongle Found:")
                        print("\tIs the YARD plugged in?")
                    
                    elif "USBTimeoutError" in line:
                        print("USBTimeoutError:")
                        print("\tYARD exited with error last time, unplug and plug it back in")

                    elif "falling back to straight Python..." in line:
                        print("Falling back to straight Python:")
                        print("\tYou can ignore this error")
                    
                    else:
                        print("Unknown error:")
                        print(line)

                elif "exit()" in line:  # exit manually by dev or automatically if rfcat finished by expect.sh
                    print("rfcat exit() detected")
                    self.rfcat_has_exited = True

            self.last_line_number_read += 1 #update read position
            
        if not self.inhibiton_detected:
            print("No inhibiton detected.")
        self.inhibiton_detected = False #reset inhibiton detection
    
    # This is to avoid the attack of constantly occupying the analyzer in reading-mode
    def send_inhibition_detected(self):
        print("Posting inhibition detected...")
        threading.Thread(target=self.detector.inhibition_detected).start()

    def has_rfcat_exited(self):
        return self.rfcat_has_exited


if __name__ == "__main__":
    pass
    analyzer = AnalyzerService("Detector()", "../logs/example/short.txt")
    analyzer.run()
    