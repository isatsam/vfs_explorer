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


class Vfs:
    """
    VFS initialises a virtual filesystem by creating the Directory objects
    for each respective directory inside a .vfs archive.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(filepath)
        self.root = self.init_root_dir()

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

    def init_root_dir(self) -> Directory:
        try:
            contents = self.open()
        except VfsError as e:
            raise VfsError('Could not open VFS contents: ', e)
        num_files, num_subdirs = self.read_root_header(contents)
        root = Directory(name=self.name, parent=None, num_subdirs=num_subdirs, num_files=num_files,
                         start=0, header_len=12, contents=contents)
        return root

    def extract_files(self, files: list = None) -> list:
        not_extracted = []
        if files:
            for file in files:
                if file.parent == self or file.parent in self.subdirs:
                    try:
                        file.extract()
                    except AttributeError:
                        not_extracted.append(file)
                else:
                    not_extracted.append(file)

        return not_extracted
