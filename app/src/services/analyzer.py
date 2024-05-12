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
        print("Analyzer service initialized.")

    def run(self):
        print("Running Analyzer service...")
        while True:
            self.check_logs()
            time.sleep(5)
    
    def check_logs(self):
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
            #then close the file so the is no concurrency problems, or stuck-reading problems. There never has beem but just in case
        for line in new_lines:
            if not self.inhibiton_detected:
                if "ffffffffff" in line: # TODO a bit more complex analysis to post less inhibitions found
                    print("Inhibitor detected")
                    self.inhibiton_detected = True
                    self.post_inhibition_detected()
                    #i want to run the post on another thread so i can continue reading the file
                    #after posting on another thread, i want to ignore
                        #inhibitors detected in same batch
                        #inhibitors detected for x time

                elif "Error" in line:
                    print("Error detected")
                    if "Access denied (insufficient permissions)" in line:
                        print("Access denied")
                        print("Did you run with sudo?")

                    elif "No Dongle Found" in line:
                        print("No Dongle Found")
                        print("Is the YARD plugged in?")
                    
                    elif "USBTimeoutError" in line:
                        print("USBTimeoutError")
                        print("YARD exited with error last time, unplug and plug it back in")

                    elif "falling back to straight Python..." in line:
                        print("Falling back to straight Python")
                        print("You can ignore this error")
                    
                    else:
                        print("Unknown error:")
                        print(line)

                elif "exit()" in line:  # exit manually by dev or automatically when rfcat finishes
                    print("Exit detected") #TODO wip make better
                    self.rfcat_has_exited = True

            self.last_line_number_read += 1 #update read position

        self.inhibiton_detected = False #reset inhibiton detection
    
    # This is to avoid the attack of constantly occupying the analyzer in reading-mode
    def post_inhibition_detected(self):
        print("Posting inhibition detected...")
        post_detection = threading.Thread(target=self.detector.post_inhibition_detected)
        post_detection.start()

    def has_rfcat_exited(self):
        return self.rfcat_has_exited


if __name__ == "__main__":
    pass
    analyzer = AnalyzerService("Detector()", "../logs/example/short.txt")
    analyzer.run()
    