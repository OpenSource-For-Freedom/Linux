import os
import time
import socket
import subprocess
from stem import Signal
from stem.control import Controller
# this came to mind reading a tor socket white page on using a remote to send inital ping then having a cross 
# remote OOB send the second. 

# Configuration for single bridge
# must have full beidge configured prior 
TORRC_CONTENT = """
UseBridges 1
Bridge obfs4 192.1.1.1:1111 ACTUAL_CERTIFICATE 
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
ControlPort 9051
"""
# be sure to add actual tor bridge ip and CA prior to launching this script 
def start_tor():
    # Start tor 
    # must have tor 
    tor_process = subprocess.Popen(['tor'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # allow time to start, maybe 8 seconds 
    return tor_process
    # Terminate the tor process
def stop_tor(tor_process):

    tor_process.terminate()
# swap identities 
def change_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())

def ping_ip_through_tor(ip_address):
    try:
        # build proxy
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

        # send 1 ping
        output = subprocess.run(["ping", "-c", "1", ip_address], capture_output=True, text=True)
        
        # Check if the ping was successful
        if output.returncode == 0:
            print(f"Ping to {ip_address} confirmed.")
            print(output.stdout)
        else:
            print(f"Ping to {ip_address} error.")
            print(output.stdout)
            print(output.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")
        
        # wouod like to add sleep function to send second ping or echo request

if __name__ == "__main__":
    ip_address = "principal_ip address"  # Replace with the IP address you want to ping 
# would like to import range of ip's

    # Start Tor
    tor_process = start_tor()
    try:
        change_tor_identity()
        ping_ip_through_tor(ip_address)
    finally:
        stop_tor(tor_process)