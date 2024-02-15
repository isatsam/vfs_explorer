import codecs
import config
from plaguevfs.core.vfs import Vfs


class Searcher:
    # TODO: iterating over files here is a bit of a cursed idea
    @staticmethod
    def search(archive: Vfs, request: str = "", results=None):
        """
        returns results in such format:
        [ printable_name, found_object ]
        """
        if not archive.files:
            config.index.index(archive)
        if not archive.files:
            return []

        request = request.lower()

        def look_in_directory(directory: Vfs, search_for, found: list):
            for item in directory.files.keys():
                if search_for in directory.files[item].filename.lower():
                    if directory.parent is None:
                        found.append([
                            codecs.decode(directory.files[item].filename, directory.encoding),
                            directory.files[item]
                        ])
                    else:
                        found.append([
                            directory.files[item].parent.name + '/' +
                            codecs.decode(directory.files[item].filename, directory.encoding),
                            directory.files[item]
                        ])
            for subdir in directory.subdirs:
                look_in_directory(subdir, search_for, found)
            return found

        if type(request) is not bytes:
            request = codecs.encode(request, archive.encoding)
        if not results:
            results = []
        results = look_in_directory(archive, request, results)
        if not results:
            raise FileNotFoundError

        return results
