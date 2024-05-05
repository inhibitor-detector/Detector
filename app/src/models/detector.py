from config import constants
import requests
import time
import json

class Detector:
    def __init__(self):
        print("Initializing Detector..")
        self.api_endpoint = constants.API_URL
        self.authorization = constants.USER + ":" + constants.PASSWORD
        self.rfcat_pid = constants.RFCAT_PID
        self.bearer_token = None
        self.refresh_token = None
        self.expires_in = None
        self.last_token_timestamp = None
        self.id = self.getId()
        print("Detector initialized.")

    def post_heartbeat(self, rfcat_failed, analyzer_failed):
        if rfcat_failed or analyzer_failed:
            print("Posting a failed heartbeat failed...")
            data = self.generate_data(isHeartbeat=True, failed=True, rfcat_failed=rfcat_failed, analyzer_failed=analyzer_failed)
        else:
            print("Posting a successfull heartbeat...")
            data = self.generate_data(isHeartbeat=True)
        url = '/signals'
        headers={'Content-Type': 'application/json'}
        self.post(url, headers, data)

    def post_inhibition_detected(self):
        print("Posting inhibition detected...")
        url = '/signals'
        headers={'Content-Type': 'application/json'}
        data = self.generate_data(isHeartbeat=False)
        self.post(url, headers, data)

    def generate_data(self, isHeartbeat, failed=False, rfcat_failed=False, analyzer_failed=False):
        data = {
                    "timestamp": time.time(), # TODO ISO_LOCAL_DATE_TIME format!
                    "detectorId": self.id,
                    "isHeartbeat": isHeartbeat
                }
        if failed:
            data["failed"] = failed
            data["rfcatFailed"] = rfcat_failed
            data["analyzerFailed"] = analyzer_failed
        return data

    def post(self, url, headers, data):
        response = requests.post(
            self.api_endpoint + url,
            headers=headers, #{'Content-Type': 'application/json',
            data=data, #'{"key": "value"}'
            auth=Authorization()
        )
        self.extract_token(response)
        print(response.status_code) 

    def get_id(self): #TODO verify this works
        response = requests.get(
            self.api_endpoint,
            headers={'Content-Type': 'application/json'},
            auth=Authorization()
        )
        if response.status_code != 200:
            print("Error getting Detector ID")
            return -1
        self.extract_token(response)
        return response.json().get('id')
    
    # TODO: check if the following works
    def extract_token(self, response):
        if response.status_code != 200:
            print("Error extracting tokens from request")
            return -1
        parsed_json = json.loads(response.text)
        self.bearer_token = parsed_json.get('access_token')
        self.refresh_token = parsed_json.get('refresh_token')
        self.expires_in = parsed_json.get('expires_in')
        self.last_token_timestamp = time.time()


class Authorization(requests.auth.AuthBase):
    def __init__(self, ):
        self.basic = (constants.USER, constants.PASSWORD)
        self.token = None #TODO implement JWT handling

    def __call__(self, r):
        return self.basic
