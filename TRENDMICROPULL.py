import requests
import json
import logging
import time
from logging.handlers import SysLogHandler
from datetime import datetime

# Configuration
API_KEY = ""
API_URL = ""
SYSLOG_SERVER = ""
SYSLOG_PORT = 

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Syslog handler
syslog_handler = SysLogHandler(address=(SYSLOG_SERVER, SYSLOG_PORT))
logger.addHandler(syslog_handler)

# Console handler for real-time output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

def query_api():
    headers = {
        "Authorization": f"Basic {API_KEY}",
        "Accept-Encoding": "gzip"
    }
    
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error querying API: {str(e)}")
        return None

def send_logs(data):
    if data and "logs" in data:
        for log in data["logs"]:
            log_message = json.dumps(log)
            logger.info(log_message)
            print(f"Sent log: {log_message[:100]}...") # Print truncated log for console readability
    else:
        print("No logs found in the response.")

def main():
    print(f"{datetime.now()} - Starting log retrieval and sending process...")
    data = query_api()
    if data:
        send_logs(data)
    else:
        print(f"{datetime.now()} - No data retrieved from API.")
    print(f"{datetime.now()} - Finished log retrieval and sending process.")

if __name__ == "__main__":
    print("Script started. Will run every 15 seconds.")
    while True:
        main()
        time.sleep(15)