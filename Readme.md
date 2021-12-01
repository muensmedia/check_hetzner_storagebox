# Nagios/Icinga2 Plugin: Monitor Disk Usage of Hetzner Storagebox

A plugin that monitors disk usage of a Hetzner StorageBox using the [Hetzner API](https://robot.your-server.de/doc/webservice/de.html#get-storagebox).
Depending on the used percentage the status (`OK`, `WARNING`, `CRITICAL` or `UNKNOWN`) is returned.

## Setup 

Downloads binary from releases and set executable bit.

    wget https://github.com/muensmedia/check_hetzner_storagebox/releases/download/latest/check_hetzner_storagebox-amd64 -O check_hetzner_storagebox
    chmod +x check_hetzner_storagebox

## CLI Usage:

    usage: check_hetzner_storagebox [-h] -u USER -p PASSWORD -id ID [-w WARNING_PERCENT] [-c CRITICAL_PERCENT]
    
    Nagios/Icinga Plugin to measure disk usage of Hetzner Storagebox via API.
    
    optional arguments:
      -h, --help            show this help message and exit
      -u USER, --user USER  Hetzner API user
      -p PASSWORD, --password PASSWORD
                            Hetzner API password
      -id ID, --identifier ID
                            ID of Hetzner Storagebox
      -w WARNING_PERCENT, --warning WARNING_PERCENT
                            Percentage threshold the status "WARNING"
      -c CRITICAL_PERCENT, --critical CRITICAL_PERCENT
                            Percentage threshold the status "CRITICAL"
