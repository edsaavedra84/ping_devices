import os
import sys
import json
import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import schedule
from loguru import logger

file_path = os.path.dirname(os.path.realpath(__file__))

# Determine config and log directories (Docker-aware)
config_dir = os.path.join(file_path, "config") if os.path.exists(os.path.join(file_path, "config")) else file_path
log_dir = os.path.join(file_path, "logs") if os.path.exists(os.path.join(file_path, "logs")) else file_path

# Configure logging to both file and console
log_file = os.path.join(log_dir, "pinging.log")
logger.add(log_file, rotation="1 day",
    retention="10 days", level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

# Add console logging (stdout)
logger.add(sys.stdout, level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

# Load configuration from config file
config_file = os.path.join(config_dir, "config.json")
interval_seconds = 30 # default
device_list = [] # default

def read_config():
    try:
        with open(config_file, 'r') as f:
            global interval_seconds
            global device_list

            config = json.load(f)
            device_list = config['devices']
            interval_seconds = config.get('interval_seconds', 30)  # Default to 30 seconds if not specified
            logger.info("Loaded {} IP addresses from config.json", len(device_list))
            logger.info("Ping interval set to {} seconds", interval_seconds)
    except FileNotFoundError:
        logger.error("config.json not found! Please create it with IP addresses to monitor.")
        exit(1)
    except json.JSONDecodeError as e:
        logger.error("Error parsing config.json: {}", str(e))
        exit(1)
    except KeyError as e:
        logger.error("Invalid config.json format. Missing key: {}", str(e))
        exit(1)    

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    try:
        out = subprocess.check_output(command)
    except BaseException as e:
        logger.debug("Platform: [{}] - Ping for: {} failed: {}", platform.system(), host, str(e))
        return False

    result = False
    
    if platform.system().lower() == "linux" or platform.system().lower() == "linux2":
        if "1 received" in str(out).lower():
            result = True
        else:
            result = False

    else:
        if "received = 1" in str(out).lower():
            result = True
        else:
            result = False

        if "unreachable" in str(out).lower():
            result = False

    if result == False:
        logger.debug("Platform: [{}] - Ping for: {} failed: {}", platform.system(), host, str(out))

    return result

def ping_all_devices():
    """Job function that pings all devices in the IP list"""
    logger.info("Reading config...")
    read_config()

    logger.info("Starting ping cycle... {}", len(device_list))
    for device in device_list:
        result = ping(device['ip'])
        logger.debug("Ping for: {:30} | IP: {:15} | Result: {:>3}", device["name"], device["ip"], "OK" if result else "NOK")
    logger.debug("-------------------")

if __name__ == "__main__":
    # Run immediately on startup
    logger.info("Starting thermostat monitoring service...")
    ping_all_devices()

    # Schedule the job to run at the specified interval
    schedule.every(interval_seconds).seconds.do(ping_all_devices)
    logger.info("Scheduled to run every {} seconds. Press Ctrl+C to stop.", interval_seconds)

    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Monitoring service stopped by user.")
