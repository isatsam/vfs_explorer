[ [English](./README.md) ] [ **Русский** ]

# VFS Explorer
Графический инструмент для просмотра и извлечения файлов из архивов формата VFS, используемого в игре "Мор. Утопия".

![Скриншот программы VFS Explorer](./screenshot_1.0.png)
[![Linux](https://github.com/isatsam/vfs_explorer/actions/workflows/linux_dev.yml/badge.svg)](https://github.com/isatsam/vfs_explorer/actions/workflows/linux_dev.yml)
 [![Windows](https://github.com/isatsam/vfs_explorer/actions/workflows/windows_dev.yml/badge.svg)](https://github.com/isatsam/vfs_explorer/actions/workflows/windows_dev.yml

# Функционал
- Просмотр содержимого архивов VFS, включая подкаталоги (папки внутри папок)
- Выборочное извлечение отдельных файлов или целых папок
- Поиск в файлах по названиям
- Поддержка русского и английского языков

# Использование
Скачать последний релиз на странице [Releases](https://github.com/isatsam/vfs_explorer/releases/latest) (в Assets под последним постом кликнуть на архив с названием нужной ОСи).
Распаковать архив и открыть программу двойным кликом, затем выбрать архив VFS.

Также при запуске через терминал можно сразу указать путь к архиву, напр. (на *nix системах): `vfs_explorer ~/Pathologic/data/Textures.vfs`

Если релиз для вашей ОСи отсутствует в списке, или вы хотите работать над кодом, то программу можно запустить из исходного кода, см. [Development.md](./Development.md#Developing).

# plaguevfs
`plaguevfs` - библиотека для парсинга, распаковки, и поиска по содержимому архивов VFS,
предоставляющая также доступ к архивам и подкаталогам изнутри архивов.
Хотя исходный код библиотеки и должен говорить сам за себя, в данный момент документация для него отсутствует.
## cli.py
cli.py - инструмент для использования `plaguevfs` через командный интерфейс.
```py
$ python cli.py --help
usage: cli.py [-h] [-a ARCHIVE] [-s SEARCH] [-x EXTRACT] [--extract_all]

options:
  -h, --help            show this help message and exit
  -a ARCHIVE, --archive ARCHIVE
                        path to the .VFS archive
  -s SEARCH, --search SEARCH
                        search for a filename (recursive)
  -x EXTRACT, --extract EXTRACT
                        extract a file by filename
  --extract_all         unpack the whole .VFS archive at once
```

# Благодарности
- somevideoguy и EGBland за их расследование формата VFS, доступное [здесь](https://github.com/somevideoguy/pathologic)
- Друзьям Марио и Джону за тестирование и нахождение ошибок в программе

# License
VFS Explorer и plaguevfs распостраняются по лицензии [GPL v3.0](./COPYING).
