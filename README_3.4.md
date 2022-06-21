devops-netology 
### Домашнее задание к занятию «3.4. Операционные системы, лекция 2»  

#### 1. Установка prometheus node_exporter
    sudo apt install prometheus-node-exporter
После установки с помощью `apt` пункты задания фактически выполнены.

    vagrant@vagrant:~$ systemctl status prometheus-node-exporter.service
    ● prometheus-node-exporter.service - Prometheus exporter for machine metrics
         Loaded: loaded (/lib/systemd/system/prometheus-node-exporter.service; enabled; vendor preset: enabled)
         Active: active (running) since Tue 2022-06-21 19:34:43 UTC; 16min ago
           Docs: https://github.com/prometheus/node_exporter
       Main PID: 12653 (prometheus-node)
          Tasks: 8 (limit: 4616)
         Memory: 1.9M
         CGroup: /system.slice/prometheus-node-exporter.service
                 └─12653 /usr/bin/prometheus-node-exporter
Сервис `prometheus-node-exporter.service` уже `enabled`, т.е. запускается автоматически.

    vagrant@vagrant:~$ cat /lib/systemd/system/prometheus-node-exporter.service
    [Unit]
    Description=Prometheus exporter for machine metrics
    Documentation=https://github.com/prometheus/node_exporter
    
    [Service]
    Restart=always
    User=prometheus
    EnvironmentFile=/etc/default/prometheus-node-exporter
    ExecStart=/usr/bin/prometheus-node-exporter $ARGS
    ExecReload=/bin/kill -HUP $MAINPID
    TimeoutStopSec=20s
    SendSIGKILL=no
    
    [Install]
    WantedBy=multi-user.target
В файле `/etc/default/prometheus-node-exporter` с помощью переменной `ARGS` задаются опции.

#### 2. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.
    curl localhost:9100/metrics | grep cpu
    curl localhost:9100/metrics | grep memory
    curl localhost:9100/metrics | grep filesystem
    curl localhost:9100/metrics | grep network
Выбранные опции (хотя все параметры не просто так отслеживаются):  
`node_cpu_seconds_total` Seconds the cpus spent in each mode.  
`node_pressure_cpu_waiting_seconds_total` Total time in seconds that processes have waited for CPU time.  
`process_cpu_seconds_total` Total user and system CPU time spent in seconds.  

`node_memory_MemTotal_bytes`  
`node_memory_MemAvailable_bytes`  
`node_memory_MemFree_bytes`  
`node_pressure_memory_stalled_seconds_total` Total time in seconds no process could make progress due to memory congestion  
`node_pressure_memory_waiting_seconds_total` Total time in seconds that processes have waited for memory  

`node_filesystem_size_bytes` Filesystem size in bytes.  
`node_filesystem_free_bytes` Filesystem free space in bytes.  
`node_filesystem_files` Filesystem total file nodes.  
`node_filesystem_files_free` Filesystem total free file nodes.  
`node_filesystem_device_error` Whether an error occurred while getting statistics for the given device.  

`node_network_receive_packets_total` Network device statistic receive_packets.  
`node_network_receive_bytes_total` Network device statistic receive_bytes.  
`node_network_receive_drop_total` Network device statistic receive_drop.  
`node_network_receive_errs_total` Network device statistic receive_errs.  
`node_network_transmit_packets_total` Network device statistic transmit_packets.  
`node_network_transmit_bytes_total` Network device statistic transmit_bytes.  
`node_network_transmit_drop_total` Network device statistic transmit_drop.  
`node_network_transmit_errs_total` Network device statistic transmit_errs.  
`node_network_speed_bytes` speed_bytes value of `/sys/class/net/<iface>`.  
`node_network_transmit_queue_length` transmit_queue_length value of `/sys/class/net/<iface>`.  

#### 3. Установите в свою виртуальную машину `Netdata`. Добавьте в Vagrantfile проброс порта `19999`.
    vagrant@vagrant:~$ sudo lsof -i :19999
    COMMAND PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    netdata 679 netdata    4u  IPv4  25833      0t0  TCP *:19999 (LISTEN)
    netdata 679 netdata   51u  IPv4  31368      0t0  TCP vagrant:19999->_gateway:3720 (ESTABLISHED)

#### 4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?
    vagrant@vagrant:~$ dmesg | grep -i virtual
    [    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
    [    0.003714] CPU MTRRs all blank - virtualized system.
    [    0.150170] Booting paravirtualized kernel on KVM
    [    5.945955] systemd[1]: Detected virtualization oracle.

#### 5. Как настроен `sysctl fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?
    vagrant@vagrant:~$ sysctl fs.nr_open
    fs.nr_open = 1048576
Это максимальное число файловых дескрипторов, которые может открыть процесс.

    # -n the maximum number of open file descriptors
    vagrant@vagrant:~$ ulimit -n
    1024
Однако `ulimit` ограничивает их число до 1024.

#### 6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под `PID 1` через `nsenter`.
    vagrant@vagrant:~$ sudo unshare -f --pid --mount-proc bash
    root@vagrant:/home/vagrant# ps
        PID TTY          TIME CMD
          1 pts/0    00:00:00 bash
          8 pts/0    00:00:00 ps
Другой терминал:  

    vagrant@vagrant:~$ ps aux | grep bash
    vagrant     1767  0.0  0.1   7368  4224 pts/0    Ss   21:03   0:00 -bash
    netdata     3447  0.0  0.0   4028  3084 ?        S    22:02   0:00 bash /usr/lib/netdata/plugins.d/tc-qos-helper.sh 1
    root        3466  0.0  0.1   9260  4688 pts/0    S    22:02   0:00 sudo unshare -f --pid --mount-proc bash
    root        3467  0.0  0.0   5480   592 pts/0    S    22:02   0:00 unshare -f --pid --mount-proc bash
    root        3468  0.0  0.1   7236  4056 pts/0    S+   22:02   0:00 bash
    vagrant     3783  0.0  0.1   7236  4172 pts/1    Ss   22:06   0:00 -bash
    vagrant     3798  0.0  0.0   6300   736 pts/1    S+   22:06   0:00 grep --color=auto bash
    vagrant@vagrant:~$ sudo nsenter --target 3468 --pid --mount
    root@vagrant:/# ps aux
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root           1  0.0  0.1   7236  4160 pts/0    S+   22:02   0:00 bash
    root          21  0.0  0.1   7236  4216 pts/1    S    22:09   0:00 -bash
    root          34  0.0  0.0   8892  3412 pts/1    R+   22:10   0:00 ps aux

#### 7. Найдите информацию о том, что такое `:(){ :|:& };:`. Вызов `dmesg` расскажет, какой механизм помогает автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?
Это Fork-бомба - вызывающая сама себя функция, которая порождает новые процессы.   

    [ 4575.712503] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope
Контроллер процессов отказался создавать новые, уперевшись в ограничение.  
Установить максимальное количество процессов можно командой вида `ulimit -u 777`.