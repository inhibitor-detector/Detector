import sys
import asyncio
from services.analyzer import AnalyzerService
from services.heartbeat import HeartbeatService
import os
from config import constants
import threading
import time
from models.detector import Detector


async def run():
    print("Initializing detector...")
    detector = Detector()
    
    print("Initializing services...")
    analyzer_service = AnalyzerService(detector, constants.LOGS_FILE)
    analyzer_thread = threading.Thread(target=analyzer_service.run)
    analyzer_thread.start()

    heartbeat_service = HeartbeatService(detector, analyzer_thread, analyzer_service)
    heartbeat_thread = threading.Thread(target=heartbeat_service.beat_start)
    heartbeat_thread.start()

def check_params():
    if len(sys.argv)!= 2:
        print(f"Usage: {sys.argv[0]} <logs_file>")
        sys.exit(1)
    if not os.path.isfile(constants.LOGS_FILE):
        print(f"Error: The logs file '{constants.LOGS_FILE}' does not exist.")
        sys.exit(1)
    if 'RFCAT_PID' not in os.environ:
        print("RFCAT_PID environment variables is not set.")
        exit(1)

if __name__ == '__main__':
    print("Starting...")
    check_params()

    asyncio.run(run())
