#!/bin/bash
# this package isntall all supported open source Linux hardening tools.
# Update package lists
sudo apt-get update

# Function to check if a package is installed
is_package_installed() {
    dpkg -l "$1" | grep -q "^ii"

# Update package lists
sudo apt-get update

# Install ClamAV if not installed
if ! is_package_installed clamav; then
    sudo apt-get install -y clamav
fi

# Install rkhunter if not installed
if ! is_package_installed rkhunter; then
    sudo apt-get install -y rkhunter
fi

# Install chkrootkit if not installed
if ! is_package_installed chkrootkit; then
    sudo apt-get install -y chkrootkit
fi

# Install Fail2Ban if not installed
if ! is_package_installed fail2ban; then
    sudo apt-get install -y fail2ban
fi

# Install Lynis if not installed
if ! is_package_installed lynis; then
    sudo apt-get install -y lynis
fi

# Install AIDE if not installed
if ! is_package_installed aide; then
    sudo apt-get install -y aide
fi

# Install AppArmor if not installed
if ! is_package_installed apparmor; then
    sudo apt-get install -y apparmor


echo "Security Tools Installed Successfully."

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
