import os
import nmap
import dpkt
import csv
import pandas as pd
import time

# IP address to scan
target_ip = "192.168.1.254"

# Specify the full path to the Nmap executable
nmap_path = "C:\Program Files (x86)\Nmap.exe"  # Replace with the actual path to Nmap

# Create a directory named "nmap scans" on the desktop if it doesn't exist
output_directory = os.path.expanduser("~/Desktop/nmap scans")
os.makedirs(output_directory, exist_ok=True)

# Function to run Nmap scan and save results to a CSV file
def run_nmap_scan(scan_command, output_filename):
    nm = nmap.PortScanner(nmap_search_path=nmap_path)
    full_output_path = os.path.join(output_directory, output_filename)
    scan_args = f"{target_ip} {scan_command}"
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

# Function to parse and analyze captured packets using dpkt
def analyze_packets(packet_data):
    # Create a list of dictionaries to store the analysis results
    analysis_results = []

    # Use dpkt to parse and analyze the packet data
    # Modify this function to perform specific packet analysis
    # For example, you can analyze packet headers, extract data, etc.
    pcap = dpkt.pcap.Reader(packet_data)

    for timestamp, buf in pcap:
        # Perform packet analysis and add results to the analysis_results list as a dictionary
        # Example: Extract relevant information from the packet and add it as key-value pairs
        analysis_result = {
            "Analysis Type": "Packet Info",
            "Timestamp": timestamp,
            "Value": "Your analysis result here"
        }
        analysis_results.append(analysis_result)

    return analysis_results

# Function to save analysis results to a CSV file
def save_analysis_to_csv(analysis_results, output_filename):
    full_output_path = os.path.join(output_directory, output_filename)
    
    # Create a DataFrame from the analysis results
    df = pd.DataFrame(analysis_results)
    
    # Save the DataFrame to a CSV file
    df.to_csv(full_output_path, index=False)

# Define scan commands
scan_commands = [
    "-sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script \"default or (discovery and safe)\"",
    "-p 1-65535 -T4 -A -v",
    "-T4 -A -v -Pn",
    "-sS -sU -T4 -A -v",
    "-T4 -F"
]

# Output filenames for each scan
output_filenames = [
    "slow_and_steady.csv",
    "intense_tcp.csv",
    "intense_ping.csv",
    "udp.csv",
    "quick.csv"
]

# Run each scan and save results to CSV files
for i in range(len(scan_commands)):
    run_nmap_scan(scan_commands[i], output_filenames[i])

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
