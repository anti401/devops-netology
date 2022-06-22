devops-netology 
### Домашнее задание к занятию «3.5. Файловые системы»  

#### 1. Узнайте о `sparse` (разряженных) файлах.
Разреженные файлы с большей эффективностью используют файловую систему. Информация о "пустых промежутках" в виде нулей хранится в блоке метаданных. Поэтому, разреженные файлы изначально занимают меньший объём носителя, чем их реальный размер.

#### 2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?
Не могут, поскольку у них одинаковый inode. Любые изменения прав применятся ко всем жёстким ссылкам.

#### 3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile.
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
    sdb                         8:16   0  2.5G  0 disk
    sdc                         8:32   0  2.5G  0 disk

#### 4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
    vagrant@vagrant:~$ sudo fdisk /dev/sdb
    
    Welcome to fdisk (util-linux 2.34).
    Changes will remain in memory only, until you decide to write them.
    Be careful before using the write command.
    
    Device does not contain a recognized partition table.
    Created a new DOS disklabel with disk identifier 0x871307ab.
    
    Command (m for help): n
    Partition type
       p   primary (0 primary, 0 extended, 4 free)
       e   extended (container for logical partitions)
    Select (default p): p
    Partition number (1-4, default 1): 1
    First sector (2048-5242879, default 2048): 2048
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G
    
    Created a new partition 1 of type 'Linux' and of size 2 GiB.
    
    Command (m for help): n
    Partition type
       p   primary (1 primary, 0 extended, 3 free)
       e   extended (container for logical partitions)
    Select (default p): p
    Partition number (2-4, default 2): 
    First sector (4196352-5242879, default 4196352):
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):
    
    Created a new partition 2 of type 'Linux' and of size 511 MiB.
    
    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.

#### 5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.
    vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb | sudo sfdisk /dev/sdc
    Checking that no-one is using this disk right now ... OK
    
    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Created a new DOS disklabel with disk identifier 0x871307ab.
    /dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
    /dev/sdc2: Created a new partition 2 of type 'Linux' and of size 511 MiB.
    /dev/sdc3: Done.
    
    New situation:
    Disklabel type: dos
    Disk identifier: 0x871307ab
    
    Device     Boot   Start     End Sectors  Size Id Type
    /dev/sdc1          2048 4196351 4194304    2G 83 Linux
    /dev/sdc2       4196352 5242879 1046528  511M 83 Linux
    
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.

#### 6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.
    vagrant@vagrant:~$ sudo mdadm --create /dev/md0 --level 1 --raid-devices 2 /dev/sdb1 /dev/sdc1
    mdadm: Note: this array has metadata at the start and
        may not be suitable as a boot device.  If you plan to
        store '/boot' on this device please ensure that
        your boot-loader understands md/v1.x metadata, or use
        --metadata=0.90
    Continue creating array? y
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md0 started.

#### 7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.
    vagrant@vagrant:~$ sudo mdadm --create /dev/md1 --level 0 --raid-devices 2 /dev/sdb2 /dev/sdc2
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md1 started.

#### 8. Создайте 2 независимых PV на получившихся md-устройствах.
    vagrant@vagrant:~$ sudo pvcreate /dev/md0 /dev/md1
      Physical volume "/dev/md0" successfully created.
      Physical volume "/dev/md1" successfully created.

#### 9. Создайте общую volume-group на этих двух PV.
    vagrant@vagrant:~$ sudo vgcreate vg0 /dev/md0 /dev/md1
      Volume group "vg0" successfully created

#### 10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.
    vagrant@vagrant:~$ sudo lvcreate --size 100M --name lv0 vg0 /dev/md1
      Logical volume "lv0" created.

#### 11. Создайте `mkfs.ext4` ФС на получившемся LV.
    vagrant@vagrant:~$ sudo mkfs.ext4 /dev/vg0/lv0
    mke2fs 1.45.5 (07-Jan-2020)
    Creating filesystem with 25600 4k blocks and 25600 inodes
    
    Allocating group tables: done
    Writing inode tables: done
    Creating journal (1024 blocks): done
    Writing superblocks and filesystem accounting information: done

#### 12. Смонтируйте этот раздел в любую директорию, например `/tmp/new`.
    vagrant@vagrant:~$ sudo mkdir /tmp/new
    vagrant@vagrant:~$ sudo mount /dev/vg0/lv0 /tmp/new

#### 13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.
    vagrant@vagrant:~$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
    ...
    2022-06-22 10:47:06 (5.30 MB/s) - ‘/tmp/new/test.gz’ saved [23711996/23711996]

#### 14. Прикрепите вывод `lsblk`.
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md0                     9:0    0    2G  0 raid1
    └─sdb2                      8:18   0  511M  0 part
      └─md1                     9:1    0 1018M  0 raid0
        └─vg0-lv0             253:1    0  100M  0 lvm   /tmp/new
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md0                     9:0    0    2G  0 raid1
    └─sdc2                      8:34   0  511M  0 part
      └─md1                     9:1    0 1018M  0 raid0
        └─vg0-lv0             253:1    0  100M  0 lvm   /tmp/new

#### 15. Протестируйте целостность файла
    vagrant@vagrant:~$ gzip -t /tmp/new/test.gz
    vagrant@vagrant:~$ echo $?
    0

#### 16. Используя `pvmove`, переместите содержимое PV с RAID0 на RAID1.
    vagrant@vagrant:~$ sudo pvmove /dev/md1 /dev/md0
      /dev/md1: Moved: 60.00%
      /dev/md1: Moved: 100.00%
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md0                     9:0    0    2G  0 raid1
    │   └─vg0-lv0             253:1    0  100M  0 lvm   /tmp/new
    └─sdb2                      8:18   0  511M  0 part
      └─md1                     9:1    0 1018M  0 raid0
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md0                     9:0    0    2G  0 raid1
    │   └─vg0-lv0             253:1    0  100M  0 lvm   /tmp/new
    └─sdc2                      8:34   0  511M  0 part
      └─md1                     9:1    0 1018M  0 raid0

#### 17. Сделайте `--fail` на устройство в вашем RAID1 md.
    vagrant@vagrant:~$ sudo mdadm /dev/md0 --fail /dev/sdc1
    mdadm: set /dev/sdc1 faulty in /dev/md0

#### 18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.
    [ 9258.863211] md/raid1:md0: Disk failure on sdc1, disabling device.
                   md/raid1:md0: Operation continuing on 1 devices.

#### 19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен.
    vagrant@vagrant:~$ gzip -t /tmp/new/test.gz
    vagrant@vagrant:~$ echo $?
    0
