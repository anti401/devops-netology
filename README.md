devops-netology 
### Домашнее задание к занятию «2.4. Инструменты Git»  

#### 1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.
    git show aefea --oneline --no-abbrev-commit
    aefead2207ef7e2aa5dc81a34aedf0cad4c32545 Update CHANGELOG.md

#### 2. Какому тегу соответствует коммит 85024d3?
v0.12.23  

    git show 85024d3
    commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)

#### 3. Сколько родителей у коммита b8d720? Напишите их хеши.
Два - 56cd7859e05c36c06b56d013b55a252d0bb7e158 и 9ea88f22fc6269854151c571162c5bcf958bee2b.  

    git show b8d720
    commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5
    Merge: 56cd7859e 9ea88f22f

    git show b8d720^
    commit 56cd7859e05c36c06b56d013b55a252d0bb7e158

    git show b8d720^2
    commit 9ea88f22fc6269854151c571162c5bcf958bee2b

#### 4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.
    git log --oneline v0.12.23..v0.12.24
    33ff1c03b (tag: v0.12.24) v0.12.24
    b14b74c49 [Website] vmc provider links
    3f235065b Update CHANGELOG.md
    6ae64e247 registry: Fix panic when server is unreachable
    5c619ca1b website: Remove links to the getting started guide's old location
    06275647e Update CHANGELOG.md
    d5f9411f5 command: Fix bug when using terraform login on Windows
    4b6d06cc5 Update CHANGELOG.md
    dd01a3507 Update CHANGELOG.md
    225466bc3 Cleanup after v0.12.23 release

#### 5. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).
Создана в 8c928e835, обновлена в 5af1e6234.

    git log -S "func providerSource" --oneline --patch
    5af1e6234 main: Honor explicit provider_installation CLI config when present
    # вывод --patch
    8c928e835 main: Consult local directories as potential mirrors of providers
    # вывод --patch

#### 6. Найдите все коммиты в которых была изменена функция globalPluginDirs.
Поиск файла с определением функции `git grep -p`, `git log -L` для поиска изменений в теле функции.

    git grep -p globalPluginDirs
    plugins.go:func globalPluginDirs() []string {

    git log -L :globalPluginDirs:plugins.go --oneline
    78b122055 Remove config.go and update things using its aliases
    # вывод diff --git a/plugins.go b/plugins.go
    52dbf9483 keep .terraform.d/plugins for discovery
    # вывод diff --git a/plugins.go b/plugins.go
    41ab0aef7 Add missing OS_ARCH dir to global plugin paths
    # вывод diff --git a/plugins.go b/plugins.go
    66ebff90c move some more plugin search path logic to command
    # вывод diff --git a/plugins.go b/plugins.go
    8364383c3 Push plugin discovery down into command package
    # вывод diff --git a/plugins.go b/plugins.go


#### 7. Кто автор функции synchronizedWriters?
Функция добавлена Martin Atkins.  

    git log -S "func synchronizedWriters" --format="%h %an (%ar) %s"
    bdfea50cc James Bardin (1 year, 6 months ago) remove unused
    5ac311e2a Martin Atkins (5 years ago) main: synchronize writes to VT100-faker on Windows
