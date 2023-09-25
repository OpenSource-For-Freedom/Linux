import os
import nmap
import csv
import time
from pythonping import ping

# Constants
TARGET_IP = "192.168.1.254"
NMAP_PATH = "C:\\Program Files (x86)\\Nmap\\nmap.exe"
OUTPUT_DIRECTORY = os.path.expanduser("~/Desktop/nmap_scans")

# Function to ping the target IP address
def ping_target(ip_address):
    try:
        response = ping(ip_address, count=4)  # Send 4 ping packets
        if response.success():
            return True
        else:
            raise Exception(f"Target IP {ip_address} is not reachable.")
    except Exception as e:
        print(f"Error: {e}")
        return False

# Function to ask the user for confirmation to proceed
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

# Function to run an Nmap scan and handle errors
def run_nmap_scan(nm, output_filename, scan_args):
    try:
        nm.scan(arguments=scan_args)
        full_output_path = os.path.join(OUTPUT_DIRECTORY, output_filename)
        with open(full_output_path, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Host", "Port/Protocol", "State", "Service"])
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    for port in lport:
                        # Extract relevant information and write it to the CSV file
                        service = nm[host][proto][port]['name']
                        state = nm[host][proto][port]['state']
                        row = [host, f"{port}/{proto}", state, service]
                        csv_writer.writerow(row)
    except Exception as e:
        print(f"An error occurred during the Nmap scan for {output_filename}: {e}")

# Check if the target is reachable by pinging it
if not ping_target(TARGET_IP):
    print(f"Terminating script because target IP {TARGET_IP} is not reachable.")
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
                nm = nmap.PortScanner(nmap_search_path=NMAP_PATH)
                scan_args = f"{TARGET_IP} {scan_commands[i]}"
                run_nmap_scan(nm, output_filenames[i], scan_args)
                
                # Sleep until the scan is completed (alternative to fixed sleep)
                while nm.still_scanning():
                    time.sleep(1)
            
            except Exception as e:
                print(f"An error occurred during the Nmap scan for {output_filenames[i]}: {e}")
        
        # Sleep for 5 seconds before saving the final CSV file
        time.sleep(5)
        
        # Capture and analyze network packets using dpkt
        # Add code for analyzing packets here (define analyze_packets function)
        
        # Save analysis results to a separate CSV file
        # Add code for saving analysis to CSV here (define save_analysis_to_csv function)
        
        print("Scans completed, and results saved to 'nmap_scans' directory on the desktop.")
        # Print a message about packet analysis
        
    else:
        print("Aborted by user.")
