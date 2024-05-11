from config import constants
import requests
import time
import json

class Detector:
    def __init__(self):
        self.api_endpoint = constants.API_URL
        self.basic_authorization = (constants.USER, constants.PASSWORD)
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
                    "timestamp": time.time(), # TODO ISO_LOCAL_DATE_TIME format!
                    "detectorId": self.id,
                    "isHeartbeat": isHeartbeat
                }
        if failed: #TODO add to API
            data["failed"] = failed
            data["rfcatFailed"] = rfcat_failed
            data["analyzerFailed"] = analyzer_failed
        return data

    def post(self, url, data):
        headers={'Content-Type': 'application/json', 'Authorization': self.get_authorization()}
        response = requests.post(
            self.api_endpoint + url,
            headers=headers, #{'Content-Type': 'application/json',
            data=data, #'{"key": "value"}'
            auth=self.get_authorization()
        )
        self.handle_response(response)
    
    def handle_response(self, response):
        print(response.status_code)
        if response.status_code == 401:
            print("401 Unauthorized")
            # TODO try again with basic auth
            return
        if response.status_code == 200:
            print("200 OK")
        if response.status_code == 201:
            print("201 Created")
        self.extract_token(response)

    def get_id(self): #TODO verify this works
        headers={'Content-Type': 'application/json', 'Authorization': self.get_authorization()}
        response = requests.get(
            self.api_endpoint,
            headers=headers,
        )
        self.handle_response(response)
        # return response.text.get('id') #TODO implement
        return 1
    
    def extract_token(self, response):
        if response.status_code != 200:
            print("Error extracting tokens from request")
            return -1
        self.bearer_token = response.headers.get('access_token')
        self.refresh_token = response.headers.get('refresh_token')
        self.expires_in = response.headers.get('expires_in')
        self.last_token_timestamp = time.time()

    def get_authorization(self):
        if self.bearer_token is None:
            return self.basic_authorization
        if time.time() - self.last_token_timestamp > self.expires_in:
            return self.basic_authorization
        return self.bearer_token
