#!/usr/bin/env python
# -*- conding: utf-8 -*-

from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from pprint import pprint
from datetime import datetime
import re

username = input("Enter your SSH username: ")
password = getpass()

start_time = datetime.now()

with open("cisco_devices_file") as f:
    devices_list = f.read().splitlines()

# print("You are going to apply the commands:\n")

for device in devices_list:
    print("Connecting to device " + device)
    ip_address_of_device = device
    ios_device = {
        "device_type": "cisco_ios",
        "ip": ip_address_of_device,
        "use_keys": False,
        "username": username,
        "password": password
    }

    sh_ip_int = f"show ip interface brief | i {device}"

    try:
        with ConnectHandler(**ios_device) as net_connect:
            intf_string = net_connect.send_command(sh_ip_int)
            interface = re.search(fr'(?P<intf>\S+)\s+(?P<address>{device})\s+', intf_string).group('intf')
            commands = [f"interface {interface}", "description MGMT"]
            output = net_connect.send_config_set(commands)
            print(output)
            with open("SUCCESSFULL_DEVICES", 'a') as f:
                f.write(ip_address_of_device + '\n')
            net_connect.save_config()
    except (AuthenticationException):
        print("Authentication failure: " + ip_address_of_device)
        with open("AUTH_FAIL", 'a') as f:
            f.write(ip_address_of_device + '\n')
        continue
    except (NetMikoTimeoutException):
        print("Timeout to device: " + ip_address_of_device)
        with open("TIMEOUT", 'a') as f:
            f.write(ip_address_of_device + '\n')
        continue
    except (EOFError):
        print("End of file while attempting device " + ip_address_of_device)
        with open("EOF", 'a') as f:
            f.write(ip_address_of_device + '\n')
        continue
    except (SSHException):
        print("SSH Issue. Are you sure SSH is enabled? " + ip_address_of_device)
        with open("SSH_err", 'a') as f:
            f.write(ip_address_of_device + '\n')
        continue
    except Exception as unknown_error:
        print("Some other error: " + str(unknown_error))
        with open("UNKNOWN_ERR", 'a') as f:
            f.write(ip_address_of_device + '\n')
        continue

end_time = datetime.now()
print("total_time = ", end_time - start_time)
