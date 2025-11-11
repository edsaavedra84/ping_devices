import os
import logging
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

file_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=file_path+'/pinging.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

#upstairs, living, playroom
ip_list = ['192.168.1.249','192.168.1.120','192.168.1.235']


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
        logging.error("Platform: [%s] - Ping for: %s failed: %s", platform.system(), host, str(e))
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
        logging.error("Platform: [%s] - Ping for: %s failed: %s", platform.system(), host, str(out))

    return result

for ip in ip_list:
    result = ping(ip)
    logging.warning("Ping for: %s was %s", ip, "OK" if result else "NOK")

logging.warning("-------------------")