#!/bin/bash 
## Script that aims to harden an initial Debian based Linux build,
## fresh out the gates with some minimum security enforcements

## e, errexit | u, nounset (treats unset variables as errors, ensuring better uniformity)
## -o pipefail, ensures that if a command in a pipeline fails, the overall exit status of
## the pipeline is the status of the last command to fail, rather
## than just the status of the last command
set -euo pipefail

## Kernel level mitigations, critical
## Note to self to do a few additional things here...
## Check if apparmor.cfg isn't already present, if it is, just add to it,
## Add a check to make sure the update-grub went correctly, few ways to do this
## Hmmm.... lots to work on!

## Copying configurations from the local grub.d to system grub.d,
## This will NOT overwrite your pre-existing values
exec_e "sudo cp -Rv ./etc/default/grub.d/* /etc/default/grub.d"

## Update grub if update-grub exists, else
## regenerate grub configuration (update-grub the older way)
if command -v update-grub &>/dev/null; then
    exec_e "sudo update-grub"
else
    exec_e "sudo grub-mkconfig -o /boot/grub/grub.cfg"
fi

## Notify user about system restart
echo 'Your system will restart in 10 seconds if you do not cancel this program'
## I should probably explain to them how to use ctrl-c...hmm..
sleep 10

## Reboot the system
exec_e "sudo reboot"

## Function to check if a package is installed
is_package_installed() {
    dpkg -l "$1" | grep -q "^ii"
}

## Log file directory
## Should we do it in /var/log/security_scans or potentially
## allow the user to input where to log (define a path variable)
## or allow them the prompt chance to disable logging? Hmm...
LOG_DIR="/var/log/security_scans"

## Ensure the log directory exists
sudo mkdir -p "$LOG_DIR"

## Date and time for log file
## Alternatively we can do %m/%d/%Y_%S%M%S, both are valid
DATE=$(date +"%Y%m%d_%H%M%S")

## Log file for script execution
SCRIPT_LOG="$LOG_DIR/script_execution_$DATE.log"
echo "Starting hard3n_8.sh execution at $(date)" | sudo tee -a "$SCRIPT_LOG"

## Function for logging
log() {
    echo "$(date +"%Y-%m-%d %T") $1" | sudo tee -a "$SCRIPT_LOG"
}

## Verify if script is executed with root privileges
if [ "$(id -u)" -ne 0 ]; then
    log "Error: Please re-run this script with sudo or as root."
    exit 1
fi

## Function to check if a command executed successfully
check_success() {
    if [ $? -ne 0 ]; then
        log "Error: $1 failed. Exiting hard3n_8.sh."
        exit 1
    else
        log "$1 completed successfully."
    fi
}

## Exec extended, logging and checking command was successful
exec_e() {
    "$@"
    check_success "$1"
}
## End note on this section, should I use hard3n_8.sh or name it after whatever the user names it as?

## Part of hardening your system is maintaining a minimized attack surface via reducing unnecessary installed applications
## APT::Sandbox::Seccomp further reading: https://lists.debian.org/debian-doc/2019/02/msg00009.html
echo 'APT::Sandbox::Seccomp "true";' | sudo tee /etc/apt/apt.conf.d/01seccomp
echo -e 'APT::AutoRemove::RecommendsImportant "false";\nAPT::Install-Recommends "0";\nAPT::Install-Suggests "0";' | sudo tee /etc/apt/apt.conf.d/01defaultrec

## Update package list
exec_e apt update

## Install ufw then enable and configure it, if not installed
if ! is_package_installed ufw; then
    exec_e apt update
    exec_e apt install -yy ufw --no-install-recommends --no-install-suggests
    exec_e ufw enable
    exec_e ufw default deny incoming
    exec_e systemctl --force --now enable ufw
    exec_e ufw reload
    exec_e ufw --force --now restart
fi

## Install and configure ClamAV, rkhunter, chkrootkit, Fail2Ban, Lynis, AIDE, and AppArmor (plus AA-extras and utils)
PACKAGES=("clamav" "rkhunter" "chkrootkit" "fail2ban" "lynis" "aide" "apparmor apparmor-profiles apparmor-profiles-extra apparmor-utils")
for package in "${PACKAGES[@]}"; do
    if ! is_package_installed "$package"; then
        execute_command apt install -yy $package --no-install-recommends --no-install-suggests
    fi
done

echo "Security Tools Installed Successfully."

## Enable strict mode, RE-enable in case anything unset
set -euo pipefail

## downstream script for more hardening like you mentioned(TCP wrappers, the boogie_man and of course lock_ness?!?! just throwing more ideas for some light weight
#utilities for this project)
source harden8_deep.sh
check_harden8_deep_success() {
    if [ $? -eq 0 ]; then
        echo "harden8_deep dependency ran successfully."
    else
        echo "Error: harden8_deep.sh did not run successfully."
        exit 1
    fi
}
#check for success
check_harden8_deep_success

## Run security scans
exec_e clamscan -r / --log="$LOG_DIR/clamav_scan_$DATE.log"
exec_e rkhunter --cronjob --update --quiet
exec_e chkrootkit | sudo tee "$LOG_DIR/chkrootkit_scan_$DATE.log"

## Notification
log "Daily security scans completed. Logs stored in $LOG_DIR"
