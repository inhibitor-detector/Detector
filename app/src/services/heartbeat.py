import os
import subprocess
import requests
from config import constants
# import jwt
import asyncio
import time
from models import detector

class HeartbeatService:
    def __init__(self, detector, analyzer_job):
        print("Initializing Heartbeat service...")
        self.detector = detector
        self.rfcat_is_running = False
        self.analyzer_is_running = False
        self.analyzer_job = analyzer_job

    def beat(self):
        while True:
            print("Heart beating...")            
            self.detector.post_heartbeat(self.check_rfcat(), self.check_analyzer())
            time.sleep(1)
    
    #TODO check if this works
    def check_rfcat(self):
        rfcat_process = subprocess.run(['ps', '-p', self.detector.rfcat_pid], stdout=subprocess.PIPE)
        if rfcat_process.stdout.decode().strip():
            self.rfcat_is_running = True
        else:
            print("RFCAT is not running.")
            self.rfcat_is_running = False
        return self.rfcat_is_running
    
    def check_analyzer(self):
        if self.analyzer_job.is_alive():
            self.analyzer_is_running = True
        else:
            print("ANALYZER is not running.")
            self.analyzer_is_running = False
        return self.analyzer_is_running
