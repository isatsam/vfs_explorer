import codecs
from .vfs import Vfs
from .embedded_file import EmbeddedFile


class Locator:
    def __init__(self, archive: Vfs):
        self.archive = archive

    # TODO: iterating over files here is a bit of a cursed idea
    def search(self, request: str = "", results=None):
        """
        returns results in such format:
        [ printable_name, found_object ]
        """

        # pre-flight checks
        if not self.archive.files:
            self.archive.files = self.archive.get_files_and_subdirs()
        if not self.archive.files:
            return []  # if there's no files then there's no files

        request = request.lower()

        # search
        def look_in_directory(directory: Vfs, search_for, found: list):
            for item in directory.files.keys():
                if search_for in directory.files[item].name.lower():
                    if directory.parent is None:
                        found.append([
                            codecs.decode(directory.files[item].name, directory.encoding),
                            directory.files[item]
                        ])
                    else:
                        found.append([
                            directory.files[item].parent.name + '/' +
                            codecs.decode(directory.files[item].name, directory.encoding),
                            directory.files[item]
                        ])
            for subdir in directory.subdirs:
                look_in_directory(subdir, search_for, found)
            return found

        if type(request) is not bytes:
            request = codecs.encode(request, self.archive.encoding)
        if not results:
            results = []
        results = look_in_directory(self.archive, request, results)
        if not results:
            raise FileNotFoundError

        return results
