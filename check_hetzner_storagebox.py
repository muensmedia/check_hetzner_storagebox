#!/usr/bin/env /usr/bin/python3

import argparse
import requests

# Mapping return codes to exit Codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Hetzner API URL
api_url = "https://api.hetzner.com/v1/storage_boxes/"

# String to give back with status, text and performance data later filled in
status_str = "{status} - {text} | {label}={value}{unit};{warn};{crit};{min};{max}"

# String to give back in case of an error, performance data intentionally without information
status_str_no_data = "{status} - {text} | UNKNOWN=0B;0;0;0;0"

def give_back(status: int, filled_in_status_str: str):
    """
    Method to give back information. Prints out message and exits with given exit Code
    :param status: Numeric exit code 0=OK,1=WARNING...
    :param filled_in_status_str: Status string to print out before exiting
    """
    print(filled_in_status_str)
    raise SystemExit(status)

def check_sb(api_key: str, id: int, warning_percent: int, critical_percent: int):
    """
    Method that accesses the Hetzner API, reads out StorageBox usage and quota and calls the give_back() method to indicate the results.
    :param api_key: API token for authorization
    :param id: StorageBox ID
    :param warning_percent: Percentage (0-100), when usage surpasses this value the status "WARNING" is issued
    :param critical_percent: Percentage (0-100), when usage surpasses this value the status "CRITICAL" is issued
    """
    
    api_header = {
        "Authorization": f"Bearer {api_key}"
    }

    # Issue GET request to API
    r = requests.get(api_url, headers=api_header)
    if r.status_code == 200:
        box_id_to_find = id
        data = r.json()["storage_boxes"]

        size_of_specific_box = next(
            (box['storage_box_type']['size'] for box in data if box['id'] == box_id_to_find),
            None
        )
        stats_of_specific_box = next(
            (
                box['stats']
                for box in data if box['id'] == box_id_to_find
            ),
            None
        )

        if size_of_specific_box is None or stats_of_specific_box is None:
            give_back(
                UNKNOWN,
                status_str_no_data.format(status="UNKNOWN", text="Specified StorageBox ID not found")
            )

        quota = size_of_specific_box
        quota_gb = round(quota / 1024**3, 0)
        used = stats_of_specific_box['size_data']
        used_gb = round(used / 1024**3, 2)
        name = next(box['name'] for box in data if box['id'] == box_id_to_find)
        warning_mb = quota * warning_percent / 100
        critical_mb = quota * critical_percent / 100

        if not name:
            name = next(box['server'] for box in data if box['id'] == box_id_to_find)
        
        percentage: int = round(used / quota * 100, 0)
        monitoring_status: int = OK
        status: str = "OK"

        if percentage >= critical_percent:
            monitoring_status = CRITICAL
            status = "CRITICAL"
        elif percentage >= warning_percent:
            monitoring_status = WARNING
            status = "WARNING"

        message = f"Storagebox {name}: {used_gb}GB of {quota_gb}GB used"
        status_long = status_str.format(
            status=status, text=message, label=name, value=used, unit="B", warn=warning_mb, crit=critical_mb, min=0, max=quota
        )
        give_back(monitoring_status, status_long)

    elif r.status_code == 404:
        give_back(UNKNOWN, status_str_no_data.format(status="UNKNOWN", text="API HTTP STATUS 404, Please check StorageBox ID"))
    elif r.status_code == 401:
        give_back(UNKNOWN, status_str_no_data.format(status="UNKNOWN", text="API HTTP STATUS 401, Please check credentials"))
    elif 500 <= r.status_code <= 599:
        give_back(UNKNOWN, status_str_no_data.format(status="UNKNOWN", text=f"API HTTP STATUS {r.status_code}, Internal Server Error at Hetzner API"))
    else:
        give_back(UNKNOWN, status_str_no_data.format(status="UNKNOWN", text=f"API HTTP STATUS {r.status_code}"))

parser = argparse.ArgumentParser(
    description='Nagios/Icinga Plugin to measure disk usage of Hetzner Storagebox via API.')
parser.add_argument('-api', '--apikey', dest='api_key', help='Hetzner API token',default="TopSecretAPIKey")
parser.add_argument('-id', '--identifier', dest='id', type=int, help='ID of Hetzner Storagebox', default=1337)
parser.add_argument('-w', '--warning', dest='warning_percent', type=int, default=90, help='Percentage threshold the status "WARNING"')
parser.add_argument('-c', '--critical', dest='critical_percent', type=int, default=95, help='Percentage threshold the status "CRITICAL"')

args = parser.parse_args()

check_sb(**vars(args))