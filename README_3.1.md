devops-netology
### Домашнее задание к занятию «3.1. Работа в терминале, лекция 1»  

#### 5. Какие ресурсы выделены виртуальной машине по-умолчанию?
2 ядра ЦП, 1024 Мб ОЗУ

#### 6. Как добавить оперативной памяти или ресурсов процессора виртуальной машине?
	config.vm.provider "virtualbox" do |v|
		v.memory = 4096
		v.cpus = 4
	end

#### 8.1 Какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?
HISTSIZE

    HISTSIZE
    The number of commands to remember in the command history (see HISTORY below).  
    If the value is 0, commands are  not  saved  in the  history  list. Numeric values 
    less than zero result in every command being saved on the history list (there is no limit). 
    The shell sets the default value to 500 after reading any startup files.

#### 8.2 Что делает директива ignoreboth в bash?
Значение HISTCONTROL, объединяет эффект значений `ignorespace` и `ignoredups` - не записывать в историю команды, которые начинаются с пробела, а также дублирующиеся команды.

#### 9. В каких сценариях использования применимы скобки `{}` и на какой строчке man bash это описано?
Выделение набора команд в единый блок.

    { list; }
    list is simply executed in the current shell environment.
    list must be terminated with a newline or semicolon. This is
    known as a group command.  The return status is the exit status of list.
    Note that unlike the metacharacters ( and ), { and } are reserved words
    and must occur where a reserved word is permitted to be recognized.
Выделение параметров, в том числе массивов.

    ${parameter}
    The value of parameter is substituted.  The braces are required when parameter is a 
    positional parameter  with  more  than  one digit,  or  when  parameter  is followed by 
    a character which is not to be interpreted as part of its name.  The parameter is a
    shell parameter as described above PARAMETERS) or an array reference (Arrays).

#### 10. Как создать однократным вызовом touch 100000 файлов? Получится ли аналогичным образом создать 300000?
    vagrant@vagrant:~$ touch {1..100000}
    # файлы создались
    vagrant@vagrant:~$ touch {1..300000}
    -bash: /usr/bin/touch: Argument list too long

#### 11. Что делает конструкция `[[ -d /tmp ]]`?
Проверяет существование директории `/tmp`.

    vagrant@vagrant:~$ if [[ -d /tmp ]]; then echo exist; fi
    exist

#### 12. Добейтесь в выводе type -a bash наличия первым пунктом в списке `bash is /tmp/new_path_directory/bash`
    vagrant@vagrant:~$ mkdir /tmp/new_path_directory/
    vagrant@vagrant:~$ touch /tmp/new_path_directory/bash
    vagrant@vagrant:~$ chmod +x /tmp/new_path_directory/bash
    vagrant@vagrant:~$ PATH=/tmp/new_path_directory:$PATH
    vagrant@vagrant:~$ type -a bash
    bash is /tmp/new_path_directory/bash
    bash is /usr/bin/bash
    bash is /bin/bash

#### 13. Чем отличается планирование команд с помощью `batch` и `at`?
`at` один раз запускает команду в определённое время.
`batch` один раз запускает команду, когда нагрузка на систему опускается до определённого порога.

    at      executes commands at a specified time.
    batch   executes commands when system load levels permit.
