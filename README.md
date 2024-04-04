# vfs_toolkit
VFS Toolkit is a tool for previewing and extracting files stored in VFS archives, such as those used in Pathologic 1.

## Features
- List contents of a VFS archive
- Select files or subdirectories to extract them
- Search through files recursively

## Installation
1. Clone this repository, or download ZIP (under the green Code button) and extract it
2. Move into the new directory
3. Ensure you have all required packages installed: `pip install -r requirements.txt`
4. Run VFS Toolkit as a module: `python -m vfs_toolkit`. Or, optionally, specify a path to a VFS archive right-away: `python -m vfs_toolkit /path/to/Archive.vfs`

## To-do list
- [X] Extract files from GUI
  - [x] Extract directories by selecting the directory's name in the tree
- [X] More reliable file search (ensure we always get the correct file and not a file with the same name from another subdirectory)
- [X] "Open archive" file prompt
- [ ] "Extract to" file prompt
- [ ] Provide pre-built binaries
- [ ] "Extract as" button, converting files to more common formats (for ex. a .tga named .tex -> .png)
- [X] Search in files
- [ ] File information layout
  - [ ] Identify file types with magic
  - [ ] Wrap around libmagic to identify Pathologic-specific file formats? (LSH, main.dat and such)
- [ ] Preview layout
  - [ ] Preview text files
  - [ ] Preview images

# plaguevfs
`plaguevfs` is a library for parsing, searching, and unpacking .VFS archives shipped with all versions of Pathologic 1
(2004 to 2015), as well as handling individual files from inside the archives and subdirectories.
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
