# vfs_toolkit
VFS Toolkit is a tool for previewing a VFS archive, such as those used in Pathologic (2005), and extracting files from it.

## Installation
1. Clone this repository
2. Move into the new directory: `cd vfs_toolkit`
3. Ensure you have all required packages installed: `pip install -r requirements.txt`
4. Run VFS Toolkit as a module with the path to the required VFS archive: `python3 -m vfs_toolkit /path/to/Archive.vfs`

## To-do list
- [X] Extract files from GUI
  - [x] Extract directories by selecting the directory's name in the tree
- [ ] More reliable file search (ensure we always get the correct file and not a file with the same name from another subdirectory)
- [ ] Provide pre-built binaries
- [ ] "Extract as" button, converting files to more common formats (for ex. a .tga named .tex -> .png)
- [ ] Search in files
- [ ] File information layout
  - [ ] Identify file types with magic
  - [ ] Wrap around libmagic to identify Pathologic-specific file formats? (LSH, main.dat and such)
- [ ] Preview layout
  - [ ] Preview text files
  - [ ] Preview images

# plaguevfs
`plaguevfs` is a library for parsing, searching, and unpacking .VFS archives shipped with all versions of Pathologic 1
(2004 to 2015), as well as individual files from inside the archives and subdirectories.
## cli.py
cli.py is a command-line tool that wraps around plaguevfs library. It currently does everything that the library can do.
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