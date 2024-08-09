# VFS Explorer
A tool for previewing and extracting files stored in VFS archives, such as those used in Pathologic 1.

![Screenshot of VFS Archive version 1.0, demonstrating a viewed archive.](./screenshot_1.0.png)

## Features
- List contents of a VFS archive
- Select files or subdirectories to extract them
- Search through files recursively

# Usage
Download a stable release for your operating system from [Releases](https://github.com/isatsam/vfs_explorer/releases/latest).
If there is no release for your OS, or you would like to run a development version, see instructions on how to run VFS Explorer in [Developing](#Developing).

## Localization
VFS Explorer supports multiple languages, and, if there's a correct translation available, it should be able to automatically select it based off
your system settings. To manually set a language, go to "Preferences" > "Language". For making VFS Explorer available in your language, see [Translating](#Translating)

# Developing
1. Clone this repository (`git clone https://github.com/isatsam/vfs_explorer.git`)
2. Move into the new directory: `cd vfs_explorer`
3. Create and activate a virtual environment: `python -m venv venv`, then source it:
   - for Unix-based systems `source ./venv/bin/activate`
   - for Windows on PowerShell: `venv\Scripts\Activate.ps1`
   - for Windows with cmd.exe: `venv\Scripts\activate.bat`
5. Install the required packages: `pip install -r requirements.txt`
6. Run: `python vfs_explorer.py`. Or, optionally, specify a path to a VFS archive right-away: `python vfs_explorer.py /path/to/Archive.vfs`

## Building
VFS Explorer is built using [PyInstaller](https://pyinstaller.org/en/stable/).
The `build_scripts` directory includes a couple scripts that are used to build the binaries in the
Releases tab of this repo. However, in general, all that's needed is:
```py
pyinstaller \
vfs_explorer.py
--name "vfs_explorer.py" \
--contents-directory "programresources" \
--noconsole \
--icon build_scripts/icon.ico  # windows-only
```
Adapt as needed for your targeted OS.
This is not necessary for development, but it's appreciated that any submitted PRs are tested for building.

## Translating
We rely on Qt's [internalization system](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html) in VFS Explorer. In particular:
  - All strings visible in the GUI must be wrapped in `tr()` or `self.tr()`.
  - QT Linguist tool is used for creating the `.qm` language files.

QT Linguist requires a `.ts` file containing all strings in the app to create a `.qm` file for a language. To (re)generate a `.ts` file, run:
```sh
pyside6-lupdate vfs_explorer/* -ts languages/ts/LanguageName.ts
```
After that, launch QT Linguist with `pyside6-linguist` and open the generated .ts file there. Once you finish providing the translated equivalents of
the strings in the .ts file, click on "File" > "Release as..." and place the new .qm file in languages/ directory.
Open VFS Explorer. If your system language corresponds to the language you just added to the app, VFS Explorer should pick it up automatically. If it doesn't,
please run: `python languages/detect.py` and rename your `.ts` and `.qm` files to the output of that command.
Check that the new language is also present in the list in "Preferences" > "Languages", then manually test the app to ensure everything looks and reads right.

# To-do list
- [X] Extract files from GUI
  - [x] Extract directories by selecting the directory's name in the tree
- [X] More reliable file search (ensure we always get the correct file and not a file with the same name from another subdirectory)
- [X] Search in files
- [X] "Open archive" file prompt
- [X] "Extract to" file prompt
- [X] Provide pre-built binaries (Windows and Linux)
    - [ ] MacOS binaries
- [X] Check for updates from inside the app
- [ ] "Extract as" button, converting files to more common formats (for ex. a .tga named .tex -> .png)
- [ ] File information layout
  - [ ] Identify file types with magic
  - [ ] Wrap around libmagic to identify Pathologic-specific file formats? (LSH, main.dat and such)
- [ ] Preview layout
  - [ ] Preview text files
  - [ ] Preview images

# plaguevfs
`plaguevfs` is a library for parsing, searching, and unpacking .VFS archives shipped with all versions of Pathologic 1
(2004 to 2015), as well as handling individual files from inside the archives and subdirectories.
Although the code aims to be as self-explanatory as possible, there's currently no documentation for the library.
## cli.py
cli.py is a command-line tool for using `plaguevfs` library from the command line.
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

# Credits
- somevideoguy and EGBland for their research on Pathologic's VFS format, available [here](https://github.com/somevideoguy/pathologic)
- Friends Mario & Jon for through testing and bug catching

# License
VFS Explorer and plaguevfs are both licensed under [GPL v3.0](./COPYING).
