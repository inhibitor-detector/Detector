import os
import subprocess
import requests
from config import constants
# import jwt

class HeartbeatService:
    def __init__(self):
        print("Initializing Heartbeat service...")
        self.rfcat_pid = constants.RFCAT_PID
        self.analyzer_pid = constants.ANALYZER_PID
        self.is_rfcat_running = False
        self.is_analyzer_running = False
        self.api_endpoint = constants.API_URL
        self.authorization = constants.USER + ":" + constants.PASSWORD
        # self.id = self.getId()
        

    def beat(self):
        print("Heart beating...")
        # self.check_rfcat()
        # self.check_analyzer()
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
        analyzer_process = subprocess.run(['ps', '-p', self.analyzer_pid], stdout=subprocess.PIPE)
        if analyzer_process.stdout.decode().strip():
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
