import sys
import asyncio
from services.analyzer import AnalyzerService
from services.heartbeat import HeartbeatService
import os
import schedule
from config import constants


async def run():
    # Initialize services
    print("Initializing services...")
    
    analyzer_service = AnalyzerService(constants.LOGS_FILE)
    (schedule.every(1).seconds
     .do(analyzer_service.analyze))

    heartbeat_service = HeartbeatService()
    (schedule.every(2).seconds
     .do(heartbeat_service.beat))
    
    schedule.run_all()

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

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
