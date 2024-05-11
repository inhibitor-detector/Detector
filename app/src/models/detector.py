# import os
# import sys
# # from dotenv import load_dotenv

# # load_dotenv()

# DETECTOR_USER="det_1_cliente_1"
# PASSWORD="12345678"
# API_URL="http://192.168.0.234:8000"



from config import constants
import requests
import time
import json
import base64
import jwt
from datetime import datetime

class Detector:
    def __init__(self):
        # self.api_endpoint = API_URL
        self.api_endpoint = constants.API_URL
        # basic_auth_string = f"{DETECTOR_USER}:{PASSWORD}"
        basic_auth_string = f"{constants.DETECTOR_USER}:{constants.PASSWORD}"
        print(basic_auth_string)
        self.basic_authorization = "Basic " + base64.b64encode(basic_auth_string.encode('utf-8')).decode('utf-8')
        print(self.basic_authorization)
        
        self.rfcat_pid = constants.RFCAT_PID
        self.bearer_token = None
        self.refresh_token = None
        self.expires_in = None
        self.last_token_timestamp = None
        self.id = self.get_id()
        print("Detector initialized.")

    def post_heartbeat(self, is_rfcat_running, is_analyzer_running):
        if is_rfcat_running and is_analyzer_running:
            print("Posting a successfull heartbeat...")
            data = self.generate_data(isHeartbeat=True)
        else:
            print("Posting a failed heartbeat failed...")
            data = self.generate_data(isHeartbeat=True, failed=True, rfcat_failed = not is_rfcat_running, analyzer_failed = not is_analyzer_running)
        url = '/signals'
        self.post(url, data)

    def post_inhibition_detected(self):
        print("Posting inhibition detected...")
        url = '/signals'
        data = self.generate_data(isHeartbeat=False)
        self.post(url, data)

    def generate_data(self, isHeartbeat, failed=False, rfcat_failed=False, analyzer_failed=False):

        data = {
                    "timestamp": datetime.now().isoformat(),
                    "detectorId": self.id,
                    "isHeartbeat": isHeartbeat
                }
        data = json.dumps(data)
        if failed: #TODO add to API
            data["failed"] = failed
            data["rfcatFailed"] = rfcat_failed
            data["analyzerFailed"] = analyzer_failed
        return data

    def post(self, url, data):
        print("posting data: ")
        print(data)
        print("posting auth: " + self.get_authorization())
        headers={'Content-Type': 'application/json', 'Authorization': self.get_authorization()}
        response = requests.post(
            self.api_endpoint + url,
            headers=headers,
            data=data,
        )
        self.handle_response(response)
    
    def handle_response(self, response):
        print(response.status_code)
        print(response.text)
        if response.status_code == 401:
            print("401 Unauthorized")
            # TODO try again with basic auth
            return
        if response.status_code == 200:
            print("200 OK")
        if response.status_code == 201:
            print("201 Created")
        self.extract_token(response)

    def get_id(self):
        headers={'Content-Type': 'application/json', 'Authorization': self.get_authorization()}
        response = requests.get(
            self.api_endpoint,
            headers=headers,
        )
        self.handle_response(response)
        # return response.text.get('id') #TODO implement, get from bearer token
        return 1
    
    def extract_token(self, response):
        self.bearer_token = response.headers.get('Authorization')
        # self.expires_in = response.headers.get('expires_in') #TODO extract from bearer token
        self.last_token_timestamp = time.time()
        # print("Bearer token: " + self.bearer_token)
        # print("Expires in: " + self.expires_in)
        # print("Last token timestamp: " + str(self.last_token_timestamp))


    def get_authorization(self):
        if self.bearer_token is None:
            return self.basic_authorization
        # if time.time() - self.last_token_timestamp > self.expires_in:
        #     return self.basic_authorization
        return self.bearer_token

if __name__ == "__main__":
    detector = Detector()
    detector.post_heartbeat(True, True)
    detector.post_inhibition_detected()