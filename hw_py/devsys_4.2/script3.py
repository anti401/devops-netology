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
