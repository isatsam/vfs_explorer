import codecs
from .directory import Directory
from .vfs import Vfs
from .embedded_file import EmbeddedFile
from .subdirectory import Subdirectory


class Indexer:
    def __init__(self):
        self.encoding = None
        self.files = None

    def index(self, archive: Vfs):
        """
        self.files format:
        { b'file_name': <EmbeddedFile object>}
        """
        self.encoding = archive.encoding
        self.files = self.index_archive(archive)

    @staticmethod
    def index_directory(directory: Directory, header_length=12):
        """
        If directory is root, header length is always 12,
        otherwise it depends on the length of the contents name in its header
        """
        if not directory.parent:
            directory.contents.seek(0)
            directory.contents.read(header_length)
        files = {}
        for i in range(directory.num_files):
            file = EmbeddedFile(parent=directory)
            name = codecs.decode(file.filename, directory.encoding).lower()
            name = codecs.encode(name, directory.encoding)
            files[name] = file
        return files

    def index_archive(self, archive: Vfs):
        def iter_index(directory):
            dictionary = self.index_directory(directory)
            for num in range(directory.num_subdirs):
                new_subdir = Subdirectory(directory.contents, directory)
                new_subdir.files = iter_index(new_subdir)
                directory.subdirs.append(new_subdir)
            return dictionary

        files = iter_index(archive)
        archive.files = files
        return files

