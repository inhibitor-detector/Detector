import sys
import asyncio
from services.analyzer import AnalyzerService
from services.heartbeat import HeartbeatService
import os
from config import constants
import threading
import time


async def run():
    # Initialize services
    print("Initializing services...")

    analyzer_service = AnalyzerService(constants.LOGS_FILE)
    analyzer_thread = threading.Thread(target=analyzer_service.run)
    analyzer_thread.start()

    heartbeat_service = HeartbeatService(analyzer_thread)
    job_thread = threading.Thread(target=heartbeat_service.beat)
    job_thread.start()

def check_params():
    if len(sys.argv)!= 2:
        print(f"Usage: {sys.argv[0]} <logs_file>")
        sys.exit(1)
    if not os.path.isfile(constants.log_file):
        print(f"Error: The logs file '{constants.log_file}' does not exist.")
        sys.exit(1)
    if 'RFCAT_PID' not in os.environ or 'ANALYZER_PID' not in os.environ:
        print("One of the PID environment variables is not set.")
        exit(1)

if __name__ == '__main__':
    print("Starting...")
    # check_params()

    asyncio.run(run())
