#!/usr/bin/env python3

import socket
import time
import json
import yaml

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
    with open('ip.json', 'w') as jsonfile:
        #json.dump(hosts, jsonfile, indent=2)
        for domain, ip in hosts.items():
            jsonfile.write(json.dumps({domain: ip}) + '\n')
    with open('ip.yaml', 'w') as yamlfile:
        yaml.dump(hosts, yamlfile)
    time.sleep(10)
