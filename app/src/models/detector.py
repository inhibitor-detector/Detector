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
        self.expires_at = None
        self.id = self.get_id()
        self.signals_url = '/signals'
        self.inhibition_detected_lock = threading.Lock()
        print("Detector initialized.")
    
    def successful_init(self):
        alarm.play_setup()

    def post_heartbeat(self, is_rfcat_running, is_analyzer_running, is_yard_running, is_memory_healthy, is_first_heartbeat):
        if is_rfcat_running and is_analyzer_running and is_yard_running and is_memory_healthy:
            print("Posting a successfull heartbeat...")
            data = self.generate_data(isHeartbeat=True, is_first_heartbeat=is_first_heartbeat)
        else:
            print("Posting a failed heartbeat...")
            failed_components = []
            if not is_rfcat_running:
                failed_components.append("RFCAT")
            if not is_analyzer_running:
                failed_components.append("ANALYZER")
            if not is_yard_running:
                failed_components.append("YARD")
            if not is_memory_healthy:
                failed_components.append("MEMORY")
            if failed_components:
                print("Failed components: " + ", ".join(failed_components))
            alarm.play_error()
            data = self.generate_data(isHeartbeat=True, failed=True, rfcat_failed=not is_rfcat_running, analyzer_failed=not is_analyzer_running, yard_failed=not is_yard_running, memory_failed=not is_memory_healthy, is_first_heartbeat=is_first_heartbeat)
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
    
    def sound_alarm_infinite(self):
        while True:
            alarm.play_error()
            time.sleep(1)

    def post_inhibition_detected(self):
        with self.inhibition_detected_lock:
            print("Posting inhibition detected...")
            data = self.generate_data(isHeartbeat=False)
            self.post(self.signals_url, data)

    def generate_data(self, isHeartbeat, failed=False, rfcat_failed=False, analyzer_failed=False, yard_failed=False, memory_failed=False, is_first_heartbeat=False):
        data = {
                    "timestamp": datetime.now().isoformat(),
                    "detectorId": self.id,
                    "isHeartbeat": isHeartbeat,
                    "acknowledged": False,
                    "status": 1,
                }
        if failed or is_first_heartbeat:
            status_bitmap = self.generate_bitmap(failed, rfcat_failed, analyzer_failed, yard_failed, memory_failed, is_first_heartbeat)
            data["status"] = status_bitmap
            print("status_bitmap:")
            print(status_bitmap)
        data = json.dumps(data)
        return data
    
    def generate_bitmap(self, failed, rfcat_failed, analyzer_failed, yard_failed, memory_failed, is_first_heartbeat):
            # bitmap: FIRST_HEARTBEAT - MEMORY_FAILED - YARD_FAILED - ANALYZER_FAILED - RFCAT_FAILED - FAILED - ACTIVE
            FIRST_HEARTBEAT = 64
            MEMORY_FAILED = 32
            YARD_FAILED = 16
            ANALYZER_FAILED = 8
            RFCAT_FAILED = 4
            FAILED = 2
            ACTIVE = 1

            bitmap = ACTIVE
            if is_first_heartbeat:
                bitmap |= FIRST_HEARTBEAT
            if memory_failed:
                bitmap |= MEMORY_FAILED
            if yard_failed:
                bitmap |= YARD_FAILED
            if analyzer_failed:
                bitmap |= ANALYZER_FAILED
            if rfcat_failed:
                bitmap |= RFCAT_FAILED
            if failed:
                bitmap |= FAILED
            return bitmap

    def post(self, url, data, must_use_basic=False):
        print("Posting data to " + self.api_endpoint + url)
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
        if response.status_code == 401:
            print("401 Unauthorized")
            return
        if response.status_code == 403:
            print("403 Forbidden Client, not authorized")
            return
        if response.status_code == 200:
            print("200 OK")
        if response.status_code == 201:
            print("201 Created")
        else:
            print("Response status code: " + str(response.status_code))
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
        return self.extract_id(response) #extrat the id from the bearer token
        
    def extract_id(self, response):
        # Extract ID from JWT token in Authorization header
        token = response.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            print("No valid bearer token found in response")
            alarm.play_error()
            return None
        try: # decode token
            token = token.split(' ')[1]
            decoded = jwt.decode(token, options={"verify_signature": False})
            detector_id = decoded.get('detectorId')
            if detector_id is None:
                print("No detector_id found in token")
                alarm.play_error()
                return None
            elif detector_id == -1: 
                print("Detector ID is -1, not valid")
                alarm.play_error()
                return None
            print("Extracted Detector ID: " + str(detector_id))
            return detector_id
        except jwt.InvalidTokenError as e:
            print(f"Failed to decode JWT token: {e}")
            alarm.play_error()
            return None

    def extract_token(self, response):
        self.bearer_token = response.headers.get('Authorization')
        if self.bearer_token and self.bearer_token.startswith('Bearer '):
            try: # decode token
                token = self.bearer_token.split(' ')[1]
                decoded = jwt.decode(token, options={"verify_signature": False})
                exp = decoded.get('exp')
                if exp:
                    self.expires_at = exp
            except jwt.InvalidTokenError as e:
                print(f"Failed to decode JWT token: {e}")
                self.expires_at = None

    def get_authorization(self, must_use_basic=False):
        if must_use_basic or self.bearer_token is None:
            return self.basic_authorization
        # if token expired, use basic auth:
        if (self.expires_at is not None and time.time() > self.expires_at):
            return self.basic_authorization
        if self.expires_at is None:
            return self.basic_authorization
        return self.bearer_token

# To execute on PC for tests. This won't run in the RPI
if __name__ == "__main__":
    constants.DETECTOR_USER="det_1_cliente_1" #dont know if this inline definition of constants.x works
    constants.PASSWORD="12345678"
    constants.API_URL="http://192.168.0.234:8000"
    detector = Detector()
    # detector.inhibition_detected()
    detector.sound_alarm()