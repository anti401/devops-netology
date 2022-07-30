#!/usr/bin/env python3

import socket
import time

hosts = {"drive.google.com": "", "mail.google.com": "", "google.com": ""}
while True:
    for host in hosts.keys():
        new_ip = socket.gethostbyname(host)
        if hosts[host] == "":
            hosts[host] = new_ip
        old_ip = hosts[host]
        if old_ip == new_ip:
            print(f'{host} - {new_ip}')
        else:
            print(f'[ERROR] {host} IP mismatch: {old_ip} {new_ip}')
            hosts[host] = new_ip
    time.sleep(10)
