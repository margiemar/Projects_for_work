#!/usr/bin/env /usr/local/adm/venv/bin/python3.9

import re
from tabulate import tabulate
from netmiko import ConnectHandler
import sys
import argparse
from argparse import RawTextHelpFormatter

#Action for interrupt
_old_excepthook = sys.excepthook
def script_excepthook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print("\n\nGlad to see you anyway!\nBye!\n")
    else:
        _old_excepthook(exctype, value, traceback)
sys.excepthook = script_excepthook



def get_log():
    parser = argparse.ArgumentParser(description='''
    ********************************************************

    The script searches for parameter in the saved logs.
    For example: log_parse 083a.886d.5f32

    ********************************************************
    ''', formatter_class=RawTextHelpFormatter)
    parser.add_argument("findme", help = "Template for search")
    args = parser.parse_args()

    linux = {
            'device_type': 'linux',
            'ip': 'IP of log server',
            'username': 'x',
            'password': 'x',
            'port': 22,
            'verbose':True
            }

    with  ConnectHandler(**linux) as connection:
        print(f"Searching {args.findme}. Thanks for waiting\n")
        output = connection.send_command(f'sudo grep -R {args.findme} /var/log/cisco')
    return output

def main():
    
    devices = dict()

    log_with_mac = get_log()

    if log_with_mac:
        
        for line in log_with_mac.split("/var/log/cisco/"):
        
            port = "UNKNOWN_PORT"
            dev = "UNKNOWN_DEVICE"
        
            try:
                 dev = re.search(r'SPB\d{2}[-]\S+', line).group().strip(":")
            except AttributeError:
                 pass
        
            if dev in devices:
                pass
            else:
                devices[dev] = set()
        
            try:
                 port = re.search(r'\S+\d{1,2}/\d{1,2}', line).group().strip(",")
                 devices[dev].add(port)
            except AttributeError:
                 pass
        
        for key, val in devices.items():
            new_key = ""
            for v in val:
                new_key = new_key + v + "\n"
            devices[key] = new_key
        
        if "UNKNOWN_DEVICE" in devices:
            if not devices["UNKNOWN_DEVICE"]: del devices["UNKNOWN_DEVICE"]
        print(tabulate(devices.items(), headers=['DEVICE', 'PORTS'], tablefmt="grid"))
    else:
        print("No results. Please, check 'logging host [IP log server]' on device")

if __name__=='__main__':
    main()

