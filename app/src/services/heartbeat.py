import os
import subprocess
from config import constants
import asyncio
import time
from models import detector

class HeartbeatService:
    def __init__(self, detector, analyzer_job, analyzer_service):
        print("Initializing Heartbeat service...")
        self.detector = detector
        self.rfcat_is_running = False
        self.analyzer_is_running = False
        self.analyzer_job = analyzer_job
        self.analyzer_service = analyzer_service
        self.memory_is_healthy = False
    
    def beat_start(self):
        while self.analyzer_service.yard_successful_init != True and self.analyzer_service.yard_successful_init != False:
            print("Waiting for YARD to initialize...")
            time.sleep(3)
        if self.analyzer_service.yard_successful_init:
            print("YARD Successful initialization")
            self.detector.successful_init()
        else:
            print("YARD Failed initialization")
            self.detector.failed_init()
        self.start_beating()

    def start_beating(self):
        while True:
            time.sleep(10)
            print("Heart beating...")            
            self.detector.post_heartbeat(self.check_rfcat(), self.check_analyzer(), self.check_memory())
    
    def check_rfcat(self):
        try:
            os.kill(self.detector.rfcat_pid, 0) # Does not kill the process, don't worry
        except OSError:                         # It only checks if PID is running
            print("RFCAT is not running.")
            self.rfcat_is_running = False
        else:
            print("RFCAT is still running.")
            self.rfcat_is_running = True

        if self.analyzer_service.has_rfcat_exited(): # For redundancy
            self.rfcat_is_running = False
        return self.rfcat_is_running
    
    def check_analyzer(self):
        if self.analyzer_job.is_alive():
            print("ANALYZER is still running.")
            self.analyzer_is_running = True
        else:
            print("ANALYZER is not running.")
            self.analyzer_is_running = False
        if self.analyzer_service.yard_error_detected:
            print("YARD error detected")
            self.analyzer_is_running = False
        return self.analyzer_is_running
    
    def check_memory(self):
        bash_command =  """
                        THRESHOLD=10; AVAILABLE_PERCENT=$(echo "scale=2; $(free -m | grep Mem | awk '{print $7}') / $(free -m | grep Mem | awk '{print $2}') * 100" | bc); SWAP_USED=$(free -m | grep Swap | awk '{print $3}'); (( $(echo "$AVAILABLE_PERCENT < $THRESHOLD" | bc -l) )) && (( $SWAP_USED > 0 )) && echo "WARNING: System is at risk of OOM! Available memory: $AVAILABLE_PERCENT%, Swap used: $SWAP_USED MB" || echo "OK: Available memory is $AVAILABLE_PERCENT%, Swap used: $SWAP_USED MB"
                        """
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()

        if "WARNING" in output:
            print(output)
            self.memory_is_healthy = False
        else:
            print(output)
            self.memory_is_healthy = True

        return self.memory_is_healthy
