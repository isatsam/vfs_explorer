import struct
import os
from .directory import Directory
from .vfs_error import VfsError
from .filesystem import Filesystem

"""
VFS header:
    4 buffer - magic numbers
    4 buffer - # of subdirs
    4 buffer - # of files
"""


class VfsArchive(Filesystem):
    """
    VFS initialises a virtual filesystem by creating the Directory objects by reading byte contents of a given .vfs file
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(filepath)
        buffer = self.open()
        self.root = self.init_root_from_header(buffer)
        super().__init__(name=self.name, root=self.root)

    def open(self):
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'rb') as file:
                if file.read(4) == b'LP1C':
                    return open(self.filepath, 'rb')
                else:
                    raise VfsError('File is not a VFS archive')
        else:
            raise FileNotFoundError(f'{self.filepath} doesn\'t exist')

    @staticmethod
    def read_root_header(buffer):
        buffer.seek(4)
        subdirs = struct.unpack('<i', buffer.read(4))[0]
        files = struct.unpack('<i', buffer.read(4))[0]
        return [files, subdirs]

    def init_root_from_header(self, buffer) -> Directory:
        num_files, num_subdirs = self.read_root_header(buffer)
        root = Directory(name=self.name, archive=self, parent=None, num_subdirs=num_subdirs, num_files=num_files,
                         start=0, header_len=12, contents=buffer)
        return root
