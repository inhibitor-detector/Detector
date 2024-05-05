import os
import subprocess
import requests
from config import constants
# import jwt
import asyncio
import time

class HeartbeatService:
    def __init__(self, analyzer_job):
        print("Initializing Heartbeat service...")
        self.rfcat_pid = constants.RFCAT_PID
        self.analyzer_pid = constants.ANALYZER_PID
        self.is_rfcat_running = False
        self.is_analyzer_running = False
        self.api_endpoint = constants.API_URL
        self.authorization = constants.USER + ":" + constants.PASSWORD
        self.analyzer_job = analyzer_job
        # self.id = self.getId()
        

    def beat(self):
        while True:
            self.check_analyzer()
            # self.check_rfcat()
            print("Heart beating...")
            time.sleep(1)
        # self.is_analyzer_running_func(self.analyzer_job_id)
        # self.post_request()
    
    def check_rfcat(self):
        rfcat_process = subprocess.run(['ps', '-p', self.rfcat_pid], stdout=subprocess.PIPE)
        if rfcat_process.stdout.decode().strip():
            print("RFCAT is running.")
            self.is_analyzer_running = True
        else:
            print("RFCAT is not running.")
            self.is_analyzer_running = False
    
    def check_analyzer(self):
        if self.analyzer_job.is_alive():
            print("ANALYZER is running.")
            self.is_analyzer_running = True
        else:
            print("ANALYZER is not running.")
            self.is_analyzer_running = False

    def post_request(self):
        response = requests.post(
            self.api_endpoint,
            headers={'Content-Type': 'application/json',
                     'Authorization': self.authorization},
            data='{"key": "value"}', #TODO construct data
            auth=('username', 'password')
        )
        print(response.status_code) 

    # Check if a specific schedule is running
    def is_analyzer_running_func(self, schedule_id):
        jobs = schedule.get_jobs()
        for job in jobs:
            if job.id == schedule_id:
                print("Analyzer is running in job: ", job)
                return True
        print("Analyzer is not running.")
        return False


    # def get_id(self): #TODO verify this works
    #     response = requests.get(
    #         self.api_endpoint,
    #         headers={'Content-Type': 'application/json',
    #                  'Authorization': self.authorization},
    #     )
    #     jwt_token = response.json().get('token')
    #     bearer_token = f"Bearer {jwt_token}" if jwt_token else None
    #     decoded_token = jwt.decode(jwt_token, algorithms=['HS256'])
    #     id = decoded_token.get('id')
    #     return id, bearer_token
