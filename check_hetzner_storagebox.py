#!/usr/bin/env python3

import argparse
import requests

# Mapping return codes to exit Codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Hetzner API URL

api_url = "https://robot-ws.your-server.de/storagebox/{id}"

# String to give back with status, text and performance data later filled in
status_str = "{status} - {text} | {label}={value} {unit};{warn};{crit};{min};{max}"

# String to give back in case of an error, performance data intentionally without information
status_str_no_data = "{status} - {text} | UNKOWN=0MB;0;0;0;0"


def give_back(status: int, filled_in_status_str: str):
    """
    Method to give back information. Prints out message and exits with given exit Code
    :param status: Numeric exit code 0=OK,1=WARNING...
    :param filled_in_status_str: Status string to print out before exiting
    """
    print(filled_in_status_str)
    raise SystemExit(status)


def check_sb(user: str, password: str, id: int, warning_percent: int, critical_percent: int):
    """
    Method that accesses the Hetzner Robot Webservice API, reads out StorageBox Usage and Quota and calls the give_back() method to indicate the results.
    :param user: API user
    :param password: API password
    :param id: StorageBox ID
    :param warning_percent: Percentage (0-100), when usage suprasses this value the status "WARNING" is issued
    :param critical_percent: Percentage (0-100), when usage surpasses this value the status "CRITICAL" is issued
    """
    # Issue GET request to API
    r = requests.get(api_url.format(id=id), auth=(user, password))
    if r.status_code == 200:
        # API request succeded
        # Parse json to Dict, access data about storagebox
        data = r.json()["storagebox"]
        # Get disk quota in MB
        quota = data["disk_quota"]
        # Calculate Quota in GB, round without decimal points as quotas are expected to be round numbers of GB
        quota_gb = round(quota / 1024, 0)
        # Get disk usage in MB
        used = data["disk_usage"]
        # Convert in GB
        used_gb = round(used / 1024, 2)
        # Get name of storagebox
        name = data["name"]
        # Calculate the MB counts from which status 'WARNING'/'CRITICAL' are issued for performance data
        warning_mb = quota * warning_percent / 100
        critical_mb = quota * critical_percent / 100
        if name == "":
            # If no name is set for storagebox default to server address
            name = data["server"]
        # Calculate percentage of used space
        percentage: int = round(used / quota * 100, 0)
        # Default to status 'OK'
        monitoring_status: int = OK
        status: str = "OK"
        if percentage >= critical_percent:
            monitoring_status = CRITICAL
            status = "CRITICAL"
        elif percentage >= warning_percent:
            monitoring_status = WARNING
            status = "WARNING"
        # Create longtext message
        message = f"Storagebox {name}: {used_gb}GB of {quota_gb}GB used"
        # Fill in status string
        status_long = status_str.format(status=status, text=message, label=name, value=used, unit="MB", warn=warning_mb, crit=critical_mb, min=0, max=quota)
        # Return the data to calles, e.g. icinga/Nagios
        give_back(monitoring_status, status_long)
    elif r.status_code == 404:
        # Storagebox not found under this user
        give_back(UNKNOWN,
                  status_str_no_data.format(status="UNKOWN", text="API HTTP STATUS 404, Please check Storagebox ID"))
    elif r.status_code == 401:
        # Credentials not valid for access
        give_back(UNKNOWN,
                  status_str_no_data.format(status="UNKOWN", text="API HTTP STATUS 401, Please check credentials"))
    elif 500 <= r.status_code <= 599:
        # Some internal server Error
        give_back(UNKNOWN, status_str_no_data.format(status="UNKOWN",
                                                     text=f"API HTTP STATUS {r.status_code}, Internal Server Error at Hetzner API"))
    else:
        # Catch all other errors
        give_back(UNKNOWN, status_str_no_data.format(status="UNKOWN", text=f"API HTTP STATUS {r.status_code}"))


parser = argparse.ArgumentParser(
    description='Nagios/Icinga Plugin to measure disk usage of Hetzner Storagebox via API.')
parser.add_argument('-u', '--user', dest='user', help='Hetzner API user', required=True)
parser.add_argument('-p', '--password', dest='password', help='Hetzner API password', required=True)
parser.add_argument('-id', '--identifier', dest='id', type=int, help='ID of Hetzner Storagebox', required=True)
parser.add_argument('-w', '--warning', dest='warning_percent', type=int, default=90,
                    help='Percentage threshold the status "WARNING"')
parser.add_argument('-c', '--critical', dest='critical_percent', type=int, default=95,
                    help='Percentage threshold the status "CRITICAL"')

args = parser.parse_args()

check_sb(**vars(args))
