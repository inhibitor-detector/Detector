from config import constants
import requests
import time
import json
import base64
import jwt
from datetime import datetime
import alarm
import threading

class Detector:
    def __init__(self):
        self.api_endpoint = constants.API_URL
        basic_auth_string = f"{constants.DETECTOR_USER}:{constants.PASSWORD}"
        self.basic_authorization = "Basic " + base64.b64encode(basic_auth_string.encode('utf-8')).decode('utf-8')
        self.rfcat_pid = int(constants.RFCAT_PID)
        self.bearer_token = None
        self.expires_in = None
        self.last_token_timestamp = None
        self.id = self.get_id()
        self.signals_url = '/signals'
        self.inhibition_detected_lock = threading.Lock()
        print("Detector initialized.")
    
    def successful_init(self):
        alarm.play_setup()
    
    def failed_init(self):
        self.post_heartbeat(False, False)
        print("Playing wrong setup beep")
        while True:
            alarm.play_error()
            time.sleep(1)

    def post_heartbeat(self, is_rfcat_running, is_analyzer_running):
        if is_rfcat_running and is_analyzer_running:
            print("Posting a successfull heartbeat...")
            data = self.generate_data(isHeartbeat=True)
        else:
            print("Playing wrong setup beep")
            alarm.play_error()
            print("Posting a failed heartbeat...")
            data = self.generate_data(isHeartbeat=True, failed=True, rfcat_failed = not is_rfcat_running, analyzer_failed = not is_analyzer_running)
        self.post(self.signals_url, data)

    def inhibition_detected(self):
        print("Detector recieved an 'Inhibition detected' signal..")
        print("Sounding alarm")
        threading.Thread(target=self.sound_alarm).start()
        print("Posting inhibition detected to server")
        threading.Thread(target=self.post_inhibition_detected).start()

    def sound_alarm(self):
        print("Sounding alarm...")
        alarm.play_alarm()

    def post_inhibition_detected(self):
        with self.inhibition_detected_lock:
            print("Posting inhibition detected...")
            data = self.generate_data(isHeartbeat=False)
            self.post(self.signals_url, data)

    def generate_data(self, isHeartbeat, failed=False, rfcat_failed=False, analyzer_failed=False):

        data = {
                    "timestamp": datetime.now().isoformat(),
                    "detectorId": self.id,
                    "isHeartbeat": isHeartbeat
                }
        if failed: #TODO add to API
            data["failed"] = failed
            data["rfcatFailed"] = rfcat_failed
            data["analyzerFailed"] = analyzer_failed
        data = json.dumps(data)
        return data

    def post(self, url, data, must_use_basic=False):
        headers={'Content-Type': 'application/json', 'Authorization': self.get_authorization(must_use_basic)}
        response = None
        try:
            response = requests.post(
                self.api_endpoint + url,
                headers=headers,
                data=data,
            )
        except requests.exceptions.RequestException as e:
            print("Post of data failed:")
            print(e)
            alarm.play_error()
            return
        
        if response.status_code == 401 and not must_use_basic:
            print("401 Unauthorized")
            print("Trying again with basic auth...")
            self.post(url, data, must_use_basic=True)

        self.handle_response(response)
    
    def handle_response(self, response):
        # print("Response:")
        # print(response.status_code)
        # print(response.text)
        if response.status_code == 401:
            print("401 Unauthorized")
            return
        if response.status_code == 200:
            print("200 OK")
        if response.status_code == 201:
            print("201 Created")
        self.extract_token(response)

    def get_id(self):
        print("Getting detector ID...")
        headers={'Content-Type': 'application/json', 'Authorization': self.get_authorization(must_use_basic=True)}
        response = None
        try:
            response = requests.get(
                self.api_endpoint,
                headers=headers,
            )
        except requests.exceptions.RequestException as e:
            print("Get of ID failed:")
            print(e)
            alarm.play_error()
            return
        
        self.handle_response(response)
        # return response.text.get('id') #TODO implement, get from bearer token
        return 1
    
    def extract_token(self, response):
        self.bearer_token = response.headers.get('Authorization')
        # self.expires_in = response.headers.get('expires_in') #TODO extract from bearer token, wait for API implementation
        self.last_token_timestamp = time.time()
        # print("Bearer token: " + self.bearer_token)
        # print("Expires in: " + self.expires_in)
        # print("Last token timestamp: " + str(self.last_token_timestamp))


    def get_authorization(self, must_use_basic=False):
        if must_use_basic or self.bearer_token is None:
            return self.basic_authorization
        # if time.time() - self.last_token_timestamp > self.expires_in: #TODO wait for implementation
        #     return self.basic_authorization
        return self.bearer_token

if __name__ == "__main__": #to execute on PC for tests. This won't run in the RPI
    constants.DETECTOR_USER="det_1_cliente_1" #dont know if this inline definition of constants.x works
    constants.PASSWORD="12345678"
    constants.API_URL="http://192.168.0.234:8000"
    detector = Detector()
    # detector.post_heartbeat(True, True)
    # detector.inhibition_detected()
    detector.sound_alarm()