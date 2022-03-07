#!/usr/bin/env python3
#Author: Vipin John Wilson
#E-mail: vipinjohnwilson@gmail.com

import os
import subprocess
import shlex
import logging
import sys

def cmd_execute(tcpdump_cmd):
    
    LOG_FILE = "tcpdump.log"
    
    # Creates a new file
    #with open(LOG_FILE, 'w') as fp:
    #    pass

    file = open(LOG_FILE,"r+")      ## Erase current content of the log file tcpdump.log
    file.truncate(0)
    file.close()
    
    logger = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO,filename=LOG_FILE,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    process = subprocess.Popen(shlex.split(tcpdump_cmd),shell=False,stdout=subprocess.PIPE)

    # Poll process.stdout to show stdout live
    while True:
        output = process.stdout.readline().decode()
        if process.poll() is not None:
            break
        if output:
            logger.log(logging.INFO, output)
            print(output.strip())
    
    rc = process.poll()
        
def form_command(ipv4_tcpdump,port_list):
    
    os1_cmd_begin = "tcpdump -nn -tttt -A -i eth0 \"(dst host "
    os1_cmd_middle = "or dst host"
    os1_cmd_end = ") "

    ip_list_len = len(ipv4_tcpdump) - 1

    for indx, val in enumerate(ipv4_tcpdump):
        if indx == 0:
            os1_cmd_begin = os1_cmd_begin + val 
        elif ((indx > 0) and (ip_list_len < len(ipv4_tcpdump))):
            os1_cmd_begin = os1_cmd_begin + " " + os1_cmd_middle + " " + val
        else:
            os1_cmd_begin = os1_cmd_begin + " " + val
    
    os1_cmd = os1_cmd_begin + os1_cmd_end
    
    os2_cmd_begin = "and (dst port "
    os2_cmd_middle = "or dst port"
    os2_cmd_end = ")\" "
    
    port_list_len = len(port_list) - 1 

    for indx, val in enumerate(port_list):
        if indx == 0:
            os2_cmd_begin = os2_cmd_begin + val 
        elif ((indx > 0) and (port_list_len < len(port_list))):
            os2_cmd_begin = os2_cmd_begin + " " + os2_cmd_middle + " " + val
        else:
            os2_cmd_begin = os2_cmd_begin + " " + val

    os2_cmd = os2_cmd_begin + os2_cmd_end
    
    return os1_cmd + os2_cmd

def is_root():
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

def usage():
    print("Usage:\n\t" + sys.argv[0] + " <port> <port>\n")
    
def main():
    is_root()
            
    ipv4_regex = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
    ip_cmd = f"ip a s eth0 | egrep -o 'inet {ipv4_regex}' | cut -d' ' -f2"
    x = os.popen(ip_cmd).read()
    ipv4_list = x.split('\n')                                                ### The split() method splits a string into a list.
    ipv4_list_without_empty = []

    for string in ipv4_list:
        if (string != ""):                                                 ### To remove empty strings from the list ips_list
            ipv4_list_without_empty.append(string)

    n = len(sys.argv)     #because sys.argv[0] is the script itself, so minus 1 is the correct number of arguments passed

    if (n - 1) > 0:
        print("\nTotal number of arguments passed: ", n-1)
    else:
        print("\nNo arguments passed\n")
        usage()
        sys.exit("Exiting...\n")

    port_list_without_empty = sys.argv[1:]
    
    tcpdump_cmd = form_command(ipv4_list_without_empty,port_list_without_empty)
    
    print("\nCommand to run:\n\n\t\t" + tcpdump_cmd) 
    
    ch = input("\nProceed? Yes|yes|Y|y / No|no|N|n: ")
    ch_lower = ch.lower()

    if (ch_lower == 'yes') | (ch_lower == 'y'):
        cmd_execute(tcpdump_cmd)
    elif (ch_lower == 'no') | (ch_lower == 'n'):
        sys.exit("\nChose to exit. Goodbye\n")
    else:
        print("\nInvalid choice\n")


if __name__ == "__main__":
    main()
