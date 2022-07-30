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
