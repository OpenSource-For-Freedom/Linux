import subprocess
import os

# IP address to scan
target_ip = "192.168.1.1"

# Create a directory named "nmap scans" on the desktop if it doesn't exist
output_directory = os.path.expanduser("~/Desktop/nmap scans")
os.makedirs(output_directory, exist_ok=True)

# Function to run Nmap scan and save results to a CSV file
def run_nmap_scan(scan_command, output_filename):
    full_output_path = os.path.join(output_directory, output_filename)
    nmap_args = scan_command.split() + [target_ip, '-oN', full_output_path]
    subprocess.run(['nmap'] + nmap_args)

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

print("Scans completed and results saved to 'nmap scans' directory on the desktop.")
