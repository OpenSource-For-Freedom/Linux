import os
import nmap
import csv
import time
import dpkt
from pythonping import ping
import schedule

# Constants
TARGET_IP = "192.168.1.254"
# Linux File Path - using a linux only file path for now
OUTPUT_DIRECTORY = "/home/54321/Desktop/scans"
# NMAP_PATH = "/usr/bin/nmap"
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
            user_input = int(input("Target Aquired. Do you want to proceed? (1 = Yes, 2 = No): "))
            if user_input == 1:
                return True
            elif user_input == 2:
                return False
            else:
                print("Invalid input. Please enter 1 to proceed or 2 to abort.")
        except ValueError:
            print("Invalid input. Please enter 1 to proceed or 2 to abort.")

# Function to run Nmap and handle errors
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

# Function to capture and analyze network packets using dpkt
def analyze_packets():
    # Add code to analyze network packets here
    
    # we can open a pcap file and iterate through the packets
    packets_data = []  # Placeholder for packet analysis data
   # add script here

    return packets_data #needs to output on seperate CSV file

# Function to save analysis results to a separate CSV file
def save_analysis_to_csv(data, filename):
    # Add code to save analysis results to a CSV file
    try:
        full_output_path = os.path.join(OUTPUT_DIRECTORY, filename)
        with open(full_output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Source IP", "Destination IP"])  # Writing header
            for row in data:
                csv_writer.writerow(row)  # Writing each row of data
        print(f"Analysis results saved to {filename}.")
    except Exception as e:
        print(f"An error occurred while saving analysis results to {filename}: {e}")

# Function to automate the script to run weekly
def run_weekly_scan():
    if not ping_target(TARGET_IP):
        print(f"Terminating script because target IP {TARGET_IP} is not reachable.")
    else:
        # Run each scan and save results to CSV files
      

        # Sleep for 5 seconds before capturing and analyzing network packets
        time.sleep(5)

        # Capture and analyze network packets using dpkt
        packet_analysis_data = analyze_packets()

        # Save analysis results to a separate CSV file
        save_analysis_to_csv(packet_analysis_data, 'packet_analysis.csv')

        print("Scans completed, and results saved to 'nmap_scans' directory on the desktop.")

# Function to set file permissions for Linux systems
def set_file_permissions(file_path, permission_code):
    try:
        os.chmod(file_path, permission_code)
        print(f"File permissions for {file_path} set to {permission_code}.")
    except Exception as e:
        print(f"An error occurred while setting file permissions: {e}")

# Function to ask the user for confirmation to proceed
def ask_user_confirmation():
    while True:
        try:
            user_input = int(input("Target Aquired. Do you want to proceed? (1 = Yes, 2 = No): "))
            if user_input == 1:
                return True
            elif user_input == 2:
                return False
            else:
                print("Invalid input. Please enter 1 to proceed or 2 to abort.")
        except ValueError:
            print("Invalid input. Please enter 1 to proceed or 2 to abort.")


# Run the first scan and prompt the user for automation
if ask_user_confirmation():
    run