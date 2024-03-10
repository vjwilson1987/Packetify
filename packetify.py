#!/usr/bin/env python3
#Author: Vipin John Wilson
#E-mail: vipinjohnwilson@gmail.com
#Profession: Infrastructure and DevOps Lead
#LinkedIn: https://www.linkedin.com/in/vipinjohnwilson/

import os
import subprocess
import shlex
import logging
import sys
import pytz
import tzlocal
import argparse

# Global variables
version = "v2.0.0"
GREEN = '\033[92m'
RESET = '\033[0m'

def cmd_execute(tcpdump_cmd):
    LOG_FILE = "tcpdump.log"
    path = 'LOG_FILE'

    with open(LOG_FILE, "w") as file:  # Create or truncate the log file
            file.truncate(0)

    logger = logging.getLogger("packetify") # Create a logger object
    logger.setLevel(logging.INFO) # Set the log level

    # Create a file handler and set its log level
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)

    # Create a stream handler (to stream to console) and set its log level
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Get the system timezone
    system_timezone = tzlocal.get_localzone()

    # Define the log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
    formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    formatter.default_msec_format = '%s.%03d'

    # Set the timezone for the formatter
    '''In this modified version:

    We import pytz and tzlocal to get the system timezone.
    We use tzlocal.get_localzone() to obtain the system timezone.
    We set the timezone for the formatter using formatter.default_timezone = pytz.timezone(str(system_timezone)), ensuring that the log messages are timestamped with the system timezone.'''
    
    formatter.default_timezone = pytz.timezone(str(system_timezone))

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    process = subprocess.Popen(shlex.split(tcpdump_cmd), shell=False, stdout=subprocess.PIPE)

    # Poll process.stdout to show stdout live
    while True:
        output = process.stdout.readline().decode()
        if process.poll() is not None:
            break
        if output:
            logger.info(output.strip())

    rc = process.poll()

def form_command(ipv4_addresses,ports):

    base_cmd = "tcpdump -nn -tttt -A -i eth0 "
    
    # Concatenate each IP address with the desired string format and join them with 'or'
    dst_hosts = '(' + ' or '.join([f"dst host {ip}" for ip in ipv4_addresses]) + ')'
    
    # Concatenate each port with the desired string format and join them with 'or'
    dst_ports = '(' + ' or '.join([f"dst port {port}" for port in ports]) + ')'

    final_cmd = base_cmd + '"' + dst_hosts + " and " + dst_ports + '"'

    return final_cmd

def get_ips():
    ipv4_regex = r'\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b'
    ip_cmd = f"ip a s eth0 | egrep -o 'inet {ipv4_regex}' | cut -d' ' -f2"
    x = os.popen(ip_cmd).read()
    ipv4_addresses = [ip for ip in x.split('\n') if ip.strip()] #strip() removes any leading or trailing whitespaces
    return ipv4_addresses

def is_root():
    if not os.geteuid() == 0:
        print("This script must be run as root.")
        sys.exit(1)
          
def main():

    is_root()

    description = GREEN + 'Packetify is a wrapper over tcpdump utility to monitor network traffic on specific ports. It is designed to run on Linux systems' + RESET
    parser = argparse.ArgumentParser(description=description, add_help=False, conflict_handler='error')

    exclusive_group = parser.add_mutually_exclusive_group() # Create a mutually exclusive group for the two options --ports and --version. This ensures that only one of the two options can be used at a time.
    exclusive_group.add_argument('--ports', nargs='+', help='List of ports to monitor') # Add the --ports option
    exclusive_group.add_argument('--version', action='version', version='Packetify {}'.format(version), help='Check the version') # Add the --version option

    args = parser.parse_args()

    if not hasattr(args, 'version') and not args.ports:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, 'version'):
        sys.exit()

    print("\nTarget ports are:", " ".join(args.ports))

    ports = args.ports

    ipv4_addresses = get_ips()  # Get the IP addresses of the machine

    tcpdump_cmd = form_command(ipv4_addresses,ports)

    print("\nCommand to run:\n\n\t\t" + tcpdump_cmd) 
    
    ch = input("\nProceed? yes|y / no|n: ").lower()

    if ch in ('yes', 'y'):
        cmd_execute(tcpdump_cmd)
    elif ch in ('no', 'n'):
        sys.exit("\nChose to exit. Goodbye.\n")
    else:
        print("\nInvalid choice.\n")

if __name__ == "__main__":
    main()
