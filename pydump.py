#!/usr/bin/env python3
#Author: Vipin John Wilson
#E-mail: vipinjohnwilson@gmail.com
#Profession: DevOps Engineer

import os
import subprocess
import shlex
import logging
import sys
import pytz
import tzlocal

def cmd_execute(tcpdump_cmd):
    LOG_FILE = "tcpdump.log"
    path = 'LOG_FILE'

    with open(LOG_FILE, "w") as file:  # Create or truncate the log file
            file.truncate(0)

    logger = logging.getLogger("pydump") # Create a logger object
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

def usage():
    print("Usage:\n\t" + sys.argv[0] + " <port> <port>\n")
    
def main():

    is_root()

    if len(sys.argv) <= 1:  #sys.argv[0] is one argument already and is the script itself
        print("\nNo arguments passed.")
        usage()
        sys.exit("Exiting...\n")

    print("\nTarget ports are:", " ".join(sys.argv[1:]))

    ports = sys.argv[1:]
    
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
