#!/bin/bash

## Function to disable core dumps + prevent core dumps
disable_core_dumps() {
    echo "Disabling core dumps..."
    echo '* hard core 0;' | sudo tee -a /etc/security/limits.conf
}

## configure TCP Wrappers and access controls as requested
configure_tcp_wrappers() {
    echo "Configuring TCP Wrappers and access controls..."

    # Deny all connections by default
    echo "ALL: ALL" | sudo tee /etc/hosts.deny

    # Specific rule for SSH: Deny all SSH connections
    # Remove this line if you want to allow SSH based on hosts.allow configuration
    echo "sshd: ALL" | sudo tee -a /etc/hosts.deny

    # Configure access.conf for non-local logins
    echo "Configuring non-local login restrictions..."
    echo "-:ALL:ALL EXCEPT LOCAL" | sudo tee -a /etc/security/access.conf
}

## Main execution starts here
# Disable core dumps
disable_core_dumps

# Configure TCP Wrappers and access controls
configure_tcp_wrappers

echo "harden8_deep Hardening complete."

