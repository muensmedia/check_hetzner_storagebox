# Nagios/Icinga2 Plugin: Monitor Disk Usage of Hetzner Storagebox
![Build tagged release](https://github.com/muensmedia/check_hetzner_storagebox/actions/workflows/build-tagged-release.yml/badge.svg)
![Build latest release](https://github.com/muensmedia/check_hetzner_storagebox/actions/workflows/build-latest-release.yml/badge.svg)


A plugin that monitors disk usage of a Hetzner StorageBox using
the [Hetzner API](https://api.hetzner.com/v1/storage_boxes). Depending on the used percentage
the status (`OK`, `WARNING`, `CRITICAL` or `UNKNOWN`) is returned.

## Preparation

- Get the credentials for the Hetzner Console API through
  the [Hetzner Console](https://console.hetzner.com)
    - You can create the API token under `Security`/`API Tokens`/`Create API Token` (DE: `Sicherheit`
      /`API Token`/`API Token hinzufügen`)
- Get the id of your storagebox
    - Through the browser
        - Access [https://console.hetzner.com](https://console.hetzner.com)
        - Enter username and password you set in the previous step
        - Go to Storage Boxes
        - under name/id in the second column is your id (without #)
    - Using cURL
        - Execute ` curl -H "Authorization: Bearer YourAPIToken" https://api.hetzner.com/v1/storage_boxes` (substitute `YourAPIToken` accordingly)
        - You will get all data from all storages you own

## Setup

Downloads binary from releases and set executable bit.

    wget https://github.com/muensmedia/check_hetzner_storagebox/releases/download/latest/check_hetzner_storagebox-amd64 -O check_hetzner_storagebox
    chmod +x check_hetzner_storagebox

## Example for Icinga2 CheckCommand

<details>
    <summary>
Click to see example for Icinga2 CheckCommand
</summary>

    object CheckCommand "check_hetzner_storagebox" {
    import "plugin-check-command"
    command = [ "/etc/icinga2-scripts/check_hetzner_storagebox" ]
    timeout = 1m
    arguments += {
            "-c" = {
                description = "Critical"
                repeat_key = false
                required = false
                value = "$critical$"
            }
            "-id" = {
                description = "ID of the Storagebox"
                repeat_key = false
                required = true
                value = "$storagebox_id$"
            }
            "-api" = {
                description = "API key"
                repeat_key = false
                required = true
                value = "$storagebox_api_key$"
            }
            "-w" = {
                description = "Warning"
                repeat_key = false
                required = true
                value = "$warning$"
            }
        }
        vars.critical = "90"
        vars.storagebox_api_key = "default-password"
        vars.warning = "80"
    }


</details>

## CLI Usage:

    usage: check_hetzner_storagebox [-h] -api SecretAPIKey -id ID [-w WARNING_PERCENT] [-c CRITICAL_PERCENT]
    
    Nagios/Icinga Plugin to measure disk usage of Hetzner Storagebox via API.
    
    optional arguments:
      -h, --help            show this help message and exit
      -api                  Hetzner API Key
      -id ID, --identifier ID
                            ID of Hetzner Storagebox
      -w WARNING_PERCENT, --warning WARNING_PERCENT
                            Percentage threshold the status "WARNING"
      -c CRITICAL_PERCENT, --critical CRITICAL_PERCENT
                            Percentage threshold the status "CRITICAL"
