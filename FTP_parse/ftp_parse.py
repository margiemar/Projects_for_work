#!/usr/bin/env python3

from getpass import getpass
import ftplib
import re, sys
from datetime import datetime

_old_excepthook = sys.excepthook
def script_excepthook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print("\n\nGlad to see you anyway!\nBye!\n")
    else:
        _old_excepthook(exctype, value, traceback)
sys.excepthook = script_excepthook


class Last_backups:
    def __init__(self, ftp_user, ftp_pass, DO_dir, host="IP FTP"):
        self.raw_dict = {}
        self.devices = set()
        self.ftp_dict = {}
        self.last_reduct = {}
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.DO_dir = DO_dir   
        self.host = host
        self.connection()
        self.unic_devices()
        self.last_backups()
    def connection(self):       #Connection establishing, getting a list of files
        try:
            with ftplib.FTP(self.host, self.ftp_user, self.ftp_pass) as con:
                lines = []
                dirs = []
                #level 1 files
                con.cwd(f'/{self.DO_dir}/')
                for file in con.nlst():
                    if self.DO_dir in file.upper():
                        self.raw_dict[file]=con.sendcmd(f'MDTM {file}')
                #level 2 files
                con.dir(lines.append)
                for x in lines: 
                    if x.startswith('d') and not ('snooping|dhcp|DHCP') in x: dirs.append(x.split()[-1])
                if dirs:
                    for dir in dirs:            
            
                            con.cwd('/')
                            con.cwd(f'/{self.DO_dir}/{dir}')
                            for file in con.nlst():
                                if self.DO_dir in file.upper():
                                    self.raw_dict[file]=con.sendcmd(f'MDTM {file}')
        except ftplib.all_errors as e:
            print('FTP error: ', e)
    def unic_devices(self):
        try:
            for key in self.raw_dict:
                self.devices.add(re.search(DO_dir+r'(.)+?(\d){2}((-|_)[1-9])?', key).group())
        except: pass
    def last_backups(self):
        try:
            for device in self.devices:
                self.ftp_dict[device]=[]
                last_update=None
                for key in self.raw_dict:
                    if device in key:
                        self.ftp_dict[device].append(datetime.strptime(self.raw_dict[key][4:12], '%Y%m%d'))
                for d in self.ftp_dict[device]:
                    if last_update == None or d > last_update:
                        last_update = d
                self.last_reduct[device]=datetime.strftime(last_update, '%d %b %Y')  
        except Exception as err: 
            print(err)   
            pass
        print('*'*40,'\n'*2)
        for ds in sorted(self.devices):
            print(ds, '---', self.last_reduct[ds])
        


if __name__=='__main__':
    ftp_user = input("FTP user: ").strip()
    ftp_pass = getpass("FTP password: ").strip()
    if len(sys.argv) > 1:
        DO_dir=sys.argv[1].upper()
    else: DO_dir=input("DO (sityXX or SITYXX): ").upper().strip()

    Last_backups(ftp_user, ftp_pass, DO_dir)
