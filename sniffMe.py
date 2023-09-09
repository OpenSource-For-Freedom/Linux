import os
import nmap
import dpkt
import csv
import pandas as pd
import time
from pythonping import ping

# IP address to scan
target_ip = "192.168.1.254"

# Specify the full path to the Nmap executable
nmap_path = "C:\\Program Files (x86)\\Nmap\\nmap.exe"  # Replace with the actual file path

# Create a directory named "nmap scans" on the desktop if it doesn't exist
output_directory = os.path.expanduser("~/Desktop/nmap scans")
os.makedirs(output_directory, exist_ok=True)

# Function to ping the target IP address
def ping_target(ip_address):
    try:
        response = ping(ip_address, count=4)  # Send 4 ping packets
        if response.success():
            return True
        else:
            raise Exception(f"Target IP {ip_address} is not reachable.")
    except Exception as e:
        print(e)
        return False

# Ask the user for confirmation to proceed
def ask_user_confirmation():
    while True:
        try:
            user_input = int(input("Target is active. Do you want to proceed? (1 = Yes, 2 = No): "))
            if user_input == 1:
                return True
            elif user_input == 2:
                return False
            else:
                print("Invalid input. Please enter 1 to proceed or 2 to abort.")
        except ValueError:
            print("Invalid input. Please enter 1 to proceed or 2 to abort.")

# Check if the target is reachable by pinging it
if not ping_target(target_ip):
    print(f"Terminating script because target IP {target_ip} is not reachable.")
else:
    # Ask the user for confirmation to proceed
    if ask_user_confirmation():
        # Run each scan and save results to CSV files
        scan_commands = [
            "-sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script \"default or (discovery and safe)\"",
            "-p 1-65535 -T4 -A -v",
            "-T4 -A -v -Pn",
            "-sS -sU -T4 -A -v",
            "-T4 -F"
        ]

        output_filenames = [
            "slow_and_steady.csv",
            "intense_tcp.csv",
            "intense_ping.csv",
            "udp.csv",
            "quick.csv"
        ]

        for i in range(len(scan_commands)):
            try:
                nm = nmap.PortScanner(nmap_search_path=nmap_path)
                full_output_path = os.path.join(output_directory, output_filenames[i])
                scan_args = f"{target_ip} {scan_commands[i]}"
                nm.scan(arguments=scan_args)
                
                # Save the results to a CSV file
                with open(full_output_path, 'w') as csvfile:
                    for host in nm.all_hosts():
                        for proto in nm[host].all_protocols():
                            lport = nm[host][proto].keys()
                            for port in lport:
                                # Extract relevant information and write it to the CSV file
                                service = nm[host][proto][port]['name']
                                state = nm[host][proto][port]['state']
                                row = f"{host},{port}/{proto},{state},{service}\n"
                                csvfile.write(row)
                
                # Sleep for 3 seconds after each scan
                time.sleep(3)
            
            except Exception as e:
                print(f"An error occurred during the Nmap scan: {e}")
        
        # Sleep for 5 seconds before saving the final CSV file
        time.sleep(5)
        
        # Capture and analyze network packets using dpkt
        with open("captured_packets.pcap", 'rb') as pcap_file:
            pcap_data = pcap_file.read()
            analysis_results = analyze_packets(pcap_data)
        
        # Save analysis results to a separate CSV file
        save_analysis_to_csv(analysis_results, "packet_analysis.csv")
        
        print("Scans completed, and results saved to 'nmap scans' directory on the desktop.")
        print("Packet analysis results saved to 'packet_analysis.csv' on the desktop.")
    
    else:
        print("Aborted by user.")
