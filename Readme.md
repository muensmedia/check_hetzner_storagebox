# Nagios/Icinga2 Plugin: Monitor Disk Usage of Hetzner Storagebox
![Build tagged release](https://github.com/muensmedia/check_hetzner_storagebox/actions/workflows/build-tagged-release.yml/badge.svg)
![Build latest release](https://github.com/muensmedia/check_hetzner_storagebox/actions/workflows/build-latest-release.yml/badge.svg)


A plugin that monitors disk usage of a Hetzner StorageBox using
the [Hetzner API](https://robot.your-server.de/doc/webservice/de.html#get-storagebox). Depending on the used percentage
the status (`OK`, `WARNING`, `CRITICAL` or `UNKNOWN`) is returned.

## Preparation

- Get the credentials for the Robot-Webservice API through
  the [Hetzner Robot Webservice User Interface](https://robot.your-server.de/)
    - You can create the credentials under `User Icon`/`Settings`/`Webservice and app Settings` (DE: `Nutzer Icon`
      /`Einstellungen`/`Webservice- und App-Einstellungen`)
    - The password is set by yourself, the username gets send to you via E-Mail
- Get the id of your storagebox
    - Through the browser
        - Access [https://robot-ws.your-server.de/storagebox](https://robot-ws.your-server.de/storagebox)
        - Enter username and password you set in the previous step
        - Now you see a JSON-String containing Information of all storageboxes in your account
        - Find the (numeric) value of the `id` field belonging to the storagebox you want to query
    - Using cURL
        - Execute `curl -u user:password https://robot-ws.your-server.de/storagebox` (substitute `user` and `password`
          accordingly)
        - Find the (numeric) value of the `id` field belonging to the storagebox you want to query

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
