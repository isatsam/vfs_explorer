import struct
import codecs
from plaguevfs.core.directory import Directory
from plaguevfs.core.embedded_file import EmbeddedFile


class Subdirectory(Directory):
    def __init__(self, byte_contents, parent):
        self.parent = parent
        self.contents = byte_contents
        self.name, self.num_subdirs, self.num_files = self.read_subdir_header()
        self.end = self.find_end(byte_contents)
        super().__init__(self.name, self.parent, self.num_files, self.num_subdirs, self.contents)

    """
    Subdir header:
    1 byte - subdir name length
    name_len bytes - subdir name
    4 bytes - # of subdirs inside
    4 bytes - # of files inside
    """
    def read_subdir_header(self):
        name_len = ord(self.contents.read(1))
        subdir_name = ""
        for s in range(name_len):
            subdir_name += codecs.decode(self.contents.read(1), encoding='iso8859-1', errors='strict')
        subdir_subdir_num = struct.unpack('<i', self.contents.read(4))[0]
        subdir_files_num = struct.unpack('<i', self.contents.read(4))[0]
        return [subdir_name, subdir_subdir_num, subdir_files_num]

    def find_end(self, byte_section):
        for num in range(self.num_subdirs):
            Subdirectory(byte_section, self.name)
        for num in range(self.num_files):
            EmbeddedFile(byte_section=byte_section)
        return byte_section.tell()
