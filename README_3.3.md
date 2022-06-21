devops-netology 
### Домашнее задание к занятию «3.3. Операционные системы, лекция 1»  

#### 1. Какой системный вызов делает команда `cd`?
    vagrant@vagrant:~$ strace /bin/bash -c 'cd /tmp' 2>&1 | grep /tmp
    execve("/bin/bash", ["/bin/bash", "-c", "cd /tmp"], 0x7fff2ade6030 /* 23 vars */) = 0
    stat("/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=4096, ...}) = 0
    chdir("/tmp")                           = 0
Искомый системный вызов `chdir("/tmp")`.

#### 2. Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.
    vagrant@vagrant:~$ strace -e trace=stat,openat file /bin/bash
    ...
    stat("/home/vagrant/.magic.mgc", 0x7fff7db64650) = -1 ENOENT (No such file or directory)
    stat("/home/vagrant/.magic", 0x7fff7db64650) = -1 ENOENT (No such file or directory)
    openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
    stat("/etc/magic", {st_mode=S_IFREG|0644, st_size=111, ...}) = 0
    openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
    openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
    openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
    openat(AT_FDCWD, "/bin/bash", O_RDONLY|O_NONBLOCK) = 3
    /bin/bash: ELF 64-bit LSB shared object, x86-64
Найдены `/etc/magic` и `/usr/share/misc/magic.mgc`.

#### 3. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла.
    truncate -s 0 /proc/$PID/fd/$FD
Где `$PID` – номер процесса, а `$FD` – номер файлового дескриптора.

#### 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?
Зомби не занимают памяти, но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.

#### 5. В iovisor BCC есть утилита `opensnoop`. На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты?
    vagrant@vagrant:~$ sudo opensnoop-bpfcc
    PID    COMM               FD ERR PATH
    886    vminfo              4   0 /var/run/utmp
    674    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
    674    dbus-daemon        19   0 /usr/share/dbus-1/system-services
    674    dbus-daemon        -1   2 /lib/dbus-1/system-services
    674    dbus-daemon        19   0 /var/lib/snapd/dbus-1/system-services/

#### 6. Какой системный вызов использует `uname -a`? Приведите цитату из `man` по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.
    vagrant@vagrant:~$ strace -e trace=uname uname -a
    uname({sysname="Linux", nodename="vagrant", ...}) = 0
    uname({sysname="Linux", nodename="vagrant", ...}) = 0
    uname({sysname="Linux", nodename="vagrant", ...}) = 0
    Linux vagrant 5.4.0-91-generic #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
Цитата из `man 2 uname`: Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.

#### 7.1 Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
`;` просто последовательно выполняет команды, `&&` прервёт выполнение при первой ошибке

#### 7.2 Есть ли смысл использовать в bash `&&`, если применить `set -e`?
    set -e; (false; echo one) | cat; echo two
    two
Пример из `man set`, в котором `echo two` выполняется. В каких-то сценариях `&&` всё же понадобится.

#### 8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?
`-e` прерывает выполнение скрипта при ненулевом коде возврата команды  
`-u` прерывает выполнение скрипта при попытке использовать незаданную переменную  
`-x` выводит исполняемые команды и их аргументы  
`-o pipefail` код возврата команды с ошибкой устанавливается кодом возврата скрипта  
Это опции для отладки скриптов.

#### 9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).
    vagrant@vagrant:~$ ps -do state | sort | uniq -c
         52 I
          1 R
         48 S
Большая часть процессов в состоянии ожидания.  
`I` - Idle kernel thread, `S` - interruptible sleep (waiting for an event to complete)