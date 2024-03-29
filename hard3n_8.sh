#!/bin/bash 
# this package isntall all supported open source Linux hardening tools.

# Function to check if a package is installed
is_package_installed() {
    dpkg -l "$1" | grep -q "^ii"

}
# Install ufw if not installed
if ! is_package_installed ufw; then
    sudo apt install -yy ufw --no-install-recommends --no-install-suggests
fi

# Install ClamAV if not installed
if ! is_package_installed clamav; then
    sudo apt install -yy clamav --no-install-recommends --no-install-suggests
fi

# Install rkhunter if not installed
if ! is_package_installed rkhunter; then
    sudo apt install -yy rkhunter --no-install-recommends --no-install-suggests
fi

# Install chkrootkit if not installed
if ! is_package_installed chkrootkit; then
    sudo apt install -yy chkrootkit --no-install-recommends --no-install-suggests
fi

# Install Fail2Ban if not installed
if ! is_package_installed fail2ban; then
    sudo apt install -yy fail2ban --no-install-recommends --no-install-suggests
fi

# Install Lynis if not installed
if ! is_package_installed lynis; then
    sudo apt install -yy lynis --no-install-recommends --no-install-suggests
fi

# Install AIDE if not installed
if ! is_package_installed aide; then
    sudo apt install -yy aide --no-install-recommends --no-install-suggests
fi
# Install AppArmor if not installed
if ! is_package_installed apparmor; then
    sudo apt-get install -yy apparmor apparmor-profiles apparmor-profiles-extra apparmor-utils --no-install-recommends --no-install-suggests
fi

# update package list
sudo apt update
sudo apt-get update


echo "Security Tools Installed Successfully."

# Automates the run sequence of ClamAV, rkhunter, and chkrootkit on a daily basis.

# Location to store scan logs
LOG_DIR="/var/log/security_scans"

# Ensure the log directory exists
sudo mkdir -p $LOG_DIR

# Date and time for log file
DATE=$(date +"%Y%m%d_%H%M%S")

# Setup and run ufw
sudo ufw enable && sudo ufw default deny incoming && sudo systemctl --force --now enable ufw && sudo ufw reload && sudo ufw --force --now restart

# Basic and fundamental hardening via TCP Wrappers
# https://en.wikipedia.org/wiki/TCP_Wrappers
echo "ALL: ALL" | sudo tee -a /etc/hosts.deny
# Disallow non-local logins, this can be kept simple or we can go more in depth
echo "-:ALL:ALL EXCEPT LOCAL" | sudo tee -a /etc/security/access.conf

# Run ClamAV scan
sudo clamscan -r / --log="$LOG_DIR/clamav_scan_$DATE.log"

# Run rkhunter
sudo rkhunter --cronjob --update --quiet

# Run chkrootkit
sudo chkrootkit | sudo tee "$LOG_DIR/chkrootkit_scan_$DATE.log"

echo "Daily security scans completed. Logs stored in $LOG_DIR"
