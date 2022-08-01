devops-netology 
### Домашнее задание к занятию «4.3. Языки разметки JSON и YAML»  

#### Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
Нужно найти и исправить все ошибки, которые допускает наш сервис
```json
{
  "info": "Sample JSON output from our service\t",
  "elements": [
    {
      "name": "first",
      "type": "server",
      "ip": 7175
    },
    {
      "name": "second",
      "type": "proxy",
      "ip": "71.78.22.43"
    }
  ]
}
```


#### Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

#### Ваш скрипт:
```python
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
        # так json-файл корректного формата:
        # json.dump(hosts, jsonfile, indent=2)
        # так вывод согласно заданию:
        for domain, ip in hosts.items():
            jsonfile.write(json.dumps({domain: ip}) + '\n')
    with open('ip.yaml', 'w') as yamlfile:
        yaml.dump(hosts, yamlfile)
    time.sleep(10)
```

#### Вывод скрипта при запуске при тестировании:
```
python.exe C:/Git/devops-netology/hw_py/devsys_4.3/script2.py
drive.google.com - 173.194.222.194
mail.google.com - 64.233.161.19
google.com - 74.125.131.101
```

#### json-файл(ы), который(е) записал ваш скрипт:
```
{"drive.google.com": "173.194.222.194"}
{"mail.google.com": "64.233.161.19"}
{"google.com": "74.125.131.101"}
```

#### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
drive.google.com: 173.194.222.194
google.com: 74.125.131.101
mail.google.com: 64.233.161.19
```