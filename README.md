# plaguevfs
`plaguevfs` is a library for parsing, searching, and unpacking .VFS archives shipped with all versions of Pathologic 1
(2004 to 2015), as well as individual files from inside the archives and subdirectories.  
# Usage
```py
>>> import plaguevfs
>>> archive = plaguevfs.Vfs('Textures.vfs')
>>> aglaja_files = archive.search('aglaja')
>>> type(aglaja_files)
<class 'dict'>
>>> for filename in aglaja_files.keys():
...    print(filename)
...
aglaja_HEAD_dxt3_LQ.tex
aglaja_HAIR_BANGS_dxt3_LQ.tex
aglaja_HAIR_dxt3_LQ.tex
aglaja_HAIR_BANGS_dxt3.tex
aglaja_HAIR_dxt3.tex
aglaja_HEAD_dxt3.tex
aglaja_HEAD.tex
UI/NPC_Aglaja.png
UI/NPC_Aglaja_b.png
>>> 
>>> aglaja_files['aglaja_HEAD.tex'].parent
<plaguevfs.vfs.Vfs object at 0x7e2934650510>
>>> aglaja_files['aglaja_HEAD.tex'].parent.name
'Textures.vfs'
>>> aglaja_files['aglaja_HEAD.tex'].extract() # retrieve a file
>>> 
>>> aglaja_files['UI/NPC_Aglaja.png'].parent
<plaguevfs.directory.Subdirectory object at 0x7e29343450d0>
>>> aglaja_files['UI/NPC_Aglaja.png'].parent.name
'UI'
>>> aglaja_files['UI/NPC_Aglaja.png'].extract() # retrieve a file from subdirectory
```

# cli.py
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