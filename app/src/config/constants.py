import os
import sys
from dotenv import load_dotenv

load_dotenv()

RFCAT_PID = os.getenv('RFCAT_PID')
ANALYZER_PID = os.getenv('ANALYZER_PID')
API_URL = os.getenv('API_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

LOGS_FILE = sys.argv[1]
