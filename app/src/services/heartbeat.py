import os
import subprocess
import requests
from config import constants
# import jwt
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

    def beat(self):
        while True:
            print("Heart beating...")            
            self.detector.post_heartbeat(self.check_rfcat(), self.check_analyzer())
            time.sleep(10)
    
    def check_rfcat(self):
        print("checking rfcat, pid: ", self.detector.rfcat_pid)
        try:
            os.kill(self.detector.rfcat_pid, 0) # Does not kill the process, don't worry
        except OSError:                         # It only checks if PID is running
            print("RFCAT is not running.")
            self.rfcat_is_running = False
        else:
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
        return self.analyzer_is_running
