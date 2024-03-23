import codecs
import os
import struct
from .embedded_file import EmbeddedFile


class Directory:
    def __init__(self, name, archive, parent, num_files, num_subdirs, start, header_len, contents):
        self.name = name
        self.archive = archive
        self.parent = parent
        self.num_files = num_files
        self.num_subdirs = num_subdirs
        self.subdirs = []
        self.encoding = 'iso8859-1'
        self.start = start
        self.header_len = header_len
        self.contents = contents
        self.files = self.read_table_of_contents()

    def __str__(self):
        return self.name

    def read_table_of_contents(self) -> dict:
        """
        Parses all defined files (filename lengths, filenames, timestamps, byte address) from the table of contents,
        which is always present after a directory's header.
        :returns: {'filename': EmbeddedFile object}
        :rtype: dict
        """

        def index_directory(directory):
            # Return to the beginning of the directory in the buffer since we're going to be iterating over files
            directory.contents.seek(directory.start + directory.header_len)
            files_in_dir = {}
            for i in range(directory.num_files):
                found_file = EmbeddedFile(parent=directory)
                name = str(found_file)
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

    def search(self, request, results: list = None) -> dict:
        """
        Recursively searches for filenames that contain the given string
        :param request: the string to search for
        :param results: an existing list of results, if we have one already
        :return: list of EmbeddedFile objects
        """
        request = request.lower()

        # search
        def look_in_directory(directory, search_for, found: dict):
            for item in directory.files.keys():
                if search_for in directory.files[item].name.lower():
                    if directory.parent is None:
                        found[str(directory.files[item])] = directory.files[item]
                    else:
                        found[str(directory.files[item].parent) + '/' + str(directory.files[item])] = \
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

    def unpack(self, requested_files: list):
        """
        Unpacks the whole directory with its subdirectories at once
        """

        def extract_directory(directory):
            if '.vfs' in directory.name:
                target_dir = directory.name[:directory.name.rfind('.vfs')]
            else:
                target_dir = directory.name

            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            os.chdir(target_dir)

            for file in directory.files.values():
                if requested_files:
                    if file in requested_files:
                        file.extract()
                else:
                    file.extract()

            for subdir in directory.subdirs:
                extract_directory(subdir)

        extract_directory(self)


class Subdirectory(Directory):
    def __init__(self, byte_contents, parent):
        self.parent = parent
        self.contents = byte_contents
        self.start = self.contents.tell()
        self.name, self.num_subdirs, self.num_files, self.header_len = self.read_subdir_header()
        super().__init__(self.name, self.parent.archive, self.parent, self.num_files, self.num_subdirs, self.start,
                         self.header_len, self.contents)

    """
    Subdir header:
    1 byte - subdir name length
    name_len buffer - subdir name
    4 buffer - # of subdirs inside
    4 buffer - # of files inside
    """

    def read_subdir_header(self):
        name_len = ord(self.contents.read(1))
        subdir_name = ""
        for s in range(name_len):
            subdir_name += codecs.decode(self.contents.read(1), encoding='iso8859-1', errors='strict')

        subdir_subdir_num = struct.unpack('<i', self.contents.read(4))[0]
        subdir_files_num = struct.unpack('<i', self.contents.read(4))[0]
        header_len = 1 + name_len + 8
        return subdir_name, subdir_subdir_num, subdir_files_num, header_len
