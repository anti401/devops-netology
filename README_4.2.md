devops-netology 
### Домашнее задание к занятию «4.2. Использование Python для решения типовых DevOps задач»  

#### Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

#### Вопросы:
| Вопрос  | Ответ |
| ------------- | ---------- |
| Какое значение будет присвоено переменной `c`?  | TypeError: unsupported operand type(s) for +: 'int' and 'str'  |
| Как получить для переменной `c` значение 12?  | str(a) + b |
| Как получить для переменной `c` значение 3?  | a + int(b) |

#### Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

#### Ваш скрипт:
```python
#!/usr/bin/env python3

import os

repo_path = "C:/Git/devops-netology"
bash_command = ["cd " + repo_path, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()

print("Изменения в репозитории " + repo_path)
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
```

#### Вывод скрипта при запуске при тестировании:
```
python.exe C:/Git/devops-netology/hw_py/devsys_4.2/script2.py
Изменения в репозитории C:/Git/devops-netology
README_4.2.md
hw_py/devsys_4.2/script2.py
hw_py/devsys_4.2/script3.py
hw_py/devsys_4.2/script4.py
Process finished with exit code 0
```

#### Обязательная задача 3
Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

#### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

if len(sys.argv) != 2:
    print('Требуется один аргумент - путь к репозиторию.')
    sys.exit(1)

repo_path = sys.argv[1]

if not os.path.exists(repo_path + '/.git'):
    print(repo_path + ' не является репозиторием.')
    sys.exit(2)

bash_command = ["cd " + repo_path, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()

print("Изменения в репозитории " + repo_path)
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
```

#### Вывод скрипта при запуске при тестировании:
```
python.exe C:/Git/devops-netology/hw_py/devsys_4.2/script3.py
Требуется один аргумент - путь к репозиторию.
Process finished with exit code 1

python.exe C:/Git/devops-netology/hw_py/devsys_4.2/script3.py C:/Git/
C:/Git/ не является репозиторием.
Process finished with exit code 2

python.exe C:/Git/devops-netology/hw_py/devsys_4.2/script3.py C:/Git/devops-netology
Изменения в репозитории C:/Git/devops-netology
README_4.2.md
hw_py/devsys_4.2/script2.py
hw_py/devsys_4.2/script3.py
hw_py/devsys_4.2/script4.py
Process finished with exit code 0
```

#### Обязательная задача 4
Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

#### Ваш скрипт:
```python
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
            # поскольку требование сравнивать с предыдущим IP - перезаписываем
            hosts[host] = new_ip
    time.sleep(10)
```

#### Вывод скрипта при запуске при тестировании:
```
python.exe C:/Git/devops-netology/hw_py/devsys_4.2/script4.py
drive.google.com - 142.251.1.194
mail.google.com - 64.233.165.18
google.com - 173.194.222.113
[ERROR] drive.google.com IP mismatch: 142.251.1.194 127.0.0.1
[ERROR] mail.google.com IP mismatch: 64.233.165.18 127.0.0.1
[ERROR] google.com IP mismatch: 173.194.222.113 127.0.0.1
drive.google.com - 127.0.0.1
mail.google.com - 127.0.0.1
google.com - 127.0.0.1
[ERROR] drive.google.com IP mismatch: 127.0.0.1 142.251.1.194
[ERROR] mail.google.com IP mismatch: 127.0.0.1 64.233.165.18
[ERROR] google.com IP mismatch: 127.0.0.1 64.233.164.113
drive.google.com - 142.251.1.194
mail.google.com - 64.233.165.18
google.com - 64.233.164.113
```