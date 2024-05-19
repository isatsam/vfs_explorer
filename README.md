# VFS Explorer
A tool for previewing and extracting files stored in VFS archives, such as those used in Pathologic 1.

## Features
- List contents of a VFS archive
- Select files or subdirectories to extract them
- Search through files recursively

# Usage
Download a release suitable for your operating system from Releases.

## Running from source
1. Clone this repository, or download ZIP (under the green Code button) and extract it
2. Move into the new directory
3. Ensure you have all required packages installed: `pip install -r requirements.txt`
    - Before doing that, Linux users will have to create a virtual environment: 
`python -m venv venv` then activate it: `source venv/bin/activate`. See [Externally Managed Environments](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)
for more information on why this is required.
4. Run VFS Explorer: `python vfs_explorer.py`. Or, optionally, specify a path to a VFS archive right-away: `python vfs_explorer.py /path/to/Archive.vfs`

# Developing
1. Clone this repository
2. Move into the new directory: `cd vfs_explorer`
3. Create and activate a virtual environment: `python -m venv venv`, then source it:
   - for Unix-based systems `source ./venv/bin/activate`
   - for Windows on PowerShell: `venv\Scripts\Activate.ps1`
   - for Windows with cmd.exe: `venv\Scripts\activate.bat`
5. Install the required packages: `pip install -r requirements.txt`  
VFS Explorer and plaguevfs both follow [PEP-8 (aka Style Guide for Python Code)](https://peps.python.org/pep-0008/) to the best of their ability, 
so an IDE that can automatically provide suggestions or correct your code by that style would probably serve you best. 
For docstrings, reStructuredText format is used.
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

# To-do list
- [X] Extract files from GUI
  - [x] Extract directories by selecting the directory's name in the tree
- [X] More reliable file search (ensure we always get the correct file and not a file with the same name from another subdirectory)
- [X] Search in files
- [X] "Open archive" file prompt
- [X] "Extract to" file prompt
- [X] Provide pre-built binaries (Windows and Linux)
    - [ ] MacOS binaries
- [ ] Check for updates & update from inside the app
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
cli.py is a command-line tool that wraps around plaguevfs library, providing its functional from the command line.
```py
$ py cli.py --help
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
- Mario & Jon for through testing and bug catching

# License
VFS Explorer and plaguevfs are both licensed under [GPL v3.0](./COPYING).