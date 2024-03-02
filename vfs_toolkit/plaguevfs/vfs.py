import struct
import os
from .directory import Directory
from .vfs_error import VfsError

"""
VFS header:
    4 bytes - magic numbers
    4 bytes - # of subdirs
    4 bytes - # of files
"""


class Vfs(Directory):
    """
    VFS is a special subclass of Directory that can generally figure out everything
        about itself by itself, using the information provided in a file's header.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(filepath)
        self.parent = None
        try:
            self.contents = self.open()
        except VfsError as e:
            raise VfsError('Could not open VFS contents: ', e)
        self.num_files, self.num_subdirs = self.read_root_header()
        super().__init__(name=self.name, parent=self.parent, num_subdirs=self.num_subdirs, num_files=self.num_files,
                         contents=self.contents)

    def open(self):
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'rb') as file:
                if file.read(4) == b'LP1C':
                    return open(self.filepath, 'rb')
                else:
                    raise VfsError('File is not a VFS archive')
        else:
            raise FileNotFoundError(f'{self.filepath} doesn\'t exist')

    def read_root_header(self):
        self.contents.seek(4)
        subdirs = struct.unpack('<i', self.contents.read(4))[0]
        files = struct.unpack('<i', self.contents.read(4))[0]
        return [files, subdirs]
