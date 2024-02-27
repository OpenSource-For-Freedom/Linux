# Linux System Security Enhancement Script

## Introduction

This script automates the installation of essential security tools on a Debian-based system to enhance its security. Additionally, it includes a script for daily security scans to keep your system protected. Please share any issues/ updates or concerns. 

## Download Script
```
hard3n_8.sh
```
## Ensure you make script executable
```bash
chmod +x hard3n_8.sh
```
## Start Script
```bash
$ sudo ./hard3n_8.sh
```
## Automate Daily with this
```bash
#!/bin/bash

# Location to store scan logs
LOG_DIR="/var/log/security_scans"

# Ensure the log directory exists
sudo mkdir -p $LOG_DIR

# Date and time for log file
DATE=$(date +"%Y%m%d_%H%M%S")

# Run ClamAV scan
sudo clamscan -r / --log="$LOG_DIR/clamav_scan_$DATE.log"

# Run rkhunter
sudo rkhunter --cronjob --update --quiet

# Run chkrootkit
sudo chkrootkit | sudo tee "$LOG_DIR/chkrootkit_scan_$DATE.log"

echo "Daily security scans completed. Logs stored in $LOG_DIR"
```
## Schedule Daily Scans with Cron
```bash
crontab -e
```
## Run script Daily, I suggest 2-3am... cooler temp's, less load.
```bash
0 2 * * * /path/to/daily_security_scan.sh
```
## Conclusion

Regularly updating and monitoring security measures is crucial for maintaining a secure system. Why wait until your first incident?

