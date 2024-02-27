#!/bin/bash
# this package isntall all supported open source Linux hardening tools.
# Update package lists
sudo apt-get update

# Function to check if a package is installed
is_package_installed() {
    dpkg -l "$1" | grep -q "^ii"

# Install ClamAV
sudo apt-get install -y clamav

# Install rkhunter
sudo apt-get install -y rkhunter

# Install chkrootkit
sudo apt-get install -y chkrootkit

# Install Fail2Ban
sudo apt-get install -y fail2ban

# Install Lynis
sudo apt-get install -y lynis

# Install AIDE
sudo apt-get install -y aide

# Install AppArmor
sudo apt-get install -y apparmor


echo "Security tools installed successfully."

# Automates the run sequence of ClamAV, rkhunter, and chkrootkit on a daily basis.

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
