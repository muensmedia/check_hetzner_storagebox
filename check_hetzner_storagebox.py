#!/usr/bin/env python3

import argparse
import requests

# Return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Hetzner API URL

api_url = "https://robot-ws.your-server.de/storagebox/{id}"

status_str = "{status} - {text} | {label}={value}{unit};{warn};{crit};{min};{max}"
status_str_no_data = "{status} - {text} | UNKOWN=0MB;0;0;0;0"


def give_back(status: int, filled_in_status_str: str):
    print(filled_in_status_str)
    raise SystemExit(status)


def check_sb(user: str, password: str, id: int, warning_percent: int, critical_percent: int):
    r = requests.get(api_url.format(id=id), auth=(user, password))
    if r.status_code == 200:
        data = r.json()["storagebox"]
        quota = data["disk_quota"]
        quota_gb = round(quota / 1024, 1)
        used = data["disk_usage"]
        used_gb = round(used / 1024, 2)
        name = data["name"]
        warning_mb = quota * warning_percent / 100
        critical_mb = quota * critical_percent / 100
        if name == "":
            name = data["server"]
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
        status_long = status_str.format(status=status, text=message, label=name, value=used, unit="MB", warn=warning_mb, crit=critical_mb, min=0, max=quota)
        give_back(monitoring_status, status_long)
    elif r.status_code == 404:
        give_back(UNKNOWN,
                  status_str_no_data.format(status="UNKOWN", text="API HTTP STATUS 404, Please check Storagebox ID"))
    elif r.status_code == 401:
        give_back(UNKNOWN,
                  status_str_no_data.format(status="UNKOWN", text="API HTTP STATUS 401, Please check credentials"))
    elif 500 <= r.status_code <= 599:
        give_back(UNKNOWN, status_str_no_data.format(status="UNKOWN",
                                                     text=f"API HTTP STATUS {r.status_code}, Internal Server Error at Hetzner API"))
    else:
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
