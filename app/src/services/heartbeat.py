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
            self.check_analyzer()
            self.check_rfcat()
            self.detector.post_heartbeat(self.rfcat_is_running, self.analyzer_is_running)
            time.sleep(1)
    
    def check_rfcat(self):
        rfcat_process = subprocess.run(['ps', '-p', self.rfcat_pid], stdout=subprocess.PIPE)
        if rfcat_process.stdout.decode().strip():
            print("RFCAT is running.")
            self.rfcat_is_running = True
        else:
            print("RFCAT is not running.")
            self.rfcat_is_running = False
    
    def check_analyzer(self):
        if self.analyzer_job.is_alive():
            print("ANALYZER is running.")
            self.analyzer_is_running = True
        else:
            print("ANALYZER is not running.")
            self.analyzer_is_running = False
