import codecs
import os
import struct
from .embedded_file import EmbeddedFile


class Directory:
    def __init__(self, name, parent, num_files, num_subdirs, start, header_len, contents):
        self.name = name
        self.parent = parent
        self.num_files = num_files
        self.num_subdirs = num_subdirs
        self.subdirs = []
        self.encoding = 'iso8859-1'
        self.start = start
        self.header_len = header_len
        self.contents = contents
        self.files = self.get_files_and_subdirs()

    def get_files_and_subdirs(self):
        def index_directory(directory):
            # Return to the beginning of the directory in the buffer since we're going to be iterating over files
            directory.contents.seek(directory.start + directory.header_len)
            files_in_dir = {}
            for i in range(directory.num_files):
                found_file = EmbeddedFile(parent=directory)
                name = codecs.decode(found_file.name, self.encoding).lower()
                files_in_dir[name] = found_file
            return files_in_dir

        def iterate_and_index(directory):
            dictionary = index_directory(directory)
            if directory.num_subdirs > 0:
                for num in range(directory.num_subdirs):
                    new_subdir = Subdirectory(byte_contents=directory.contents, parent=directory)
                    new_subdir.files = iterate_and_index(new_subdir)
                    directory.subdirs.append(new_subdir)
            return dictionary

        files = iterate_and_index(self)
        return files

    def search(self, request, results=None):
        request = request.lower()

        # search
        def look_in_directory(directory, search_for, found: list):
            for item in directory.files.keys():
                if search_for in directory.files[item].name.lower():
                    if directory.parent is None:
                        found[directory.files[item].name.decode(directory.encoding)] = \
                            directory.files[item]
                    else:
                        found[directory.files[item].parent.name + '/' + \
                              directory.files[item].name.decode(directory.encoding)] = \
                            directory.files[item]
            for subdir in directory.subdirs:
                look_in_directory(subdir, search_for, found)
            return found

        if type(request) is not bytes:
            request = codecs.encode(request, self.encoding)
        if not results:
            results = {}
        results = look_in_directory(self, request, results)
        if not results:
            raise FileNotFoundError

        return results

    def unpack(self):
        def unpack_directory(directory):
            if '.vfs' in directory.name:
                target_dir = directory.name[:directory.name.rfind('.vfs')]
            else:
                target_dir = directory.name

            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            os.chdir(target_dir)

            for file in directory.files.values():
                directory.contents.seek(file.start)
                file_contents = directory.contents.read(file.length)
                target = file.name
                with open(target, 'wb') as t:
                    t.write(file_contents)

            for subdir in directory.subdirs:
                unpack_directory(subdir)

        unpack_directory(self)


class Subdirectory(Directory):
    def __init__(self, byte_contents, parent):
        self.parent = parent
        self.contents = byte_contents
        self.start = self.contents.tell()
        self.name, self.num_subdirs, self.num_files, self.header_len = self.read_subdir_header()
        super().__init__(self.name, self.parent, self.num_files, self.num_subdirs, self.start, self.header_len,
                         self.contents)

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
        header_len = 1 + name_len + 8
        return [subdir_name, subdir_subdir_num, subdir_files_num, header_len]
