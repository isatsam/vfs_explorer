from .directory import Directory


class Filesystem:
    def __init__(self, name: str, root: Directory, filepath: str = None):
        self.name = name
        self.root = root
        self.filepath = filepath

    def extract_files(self, files: list = None) -> list:
        not_extracted = []
        if files:
            for file in files:
                if file.parent == self.root or file.parent in self.root.subdirs:
                    try:
                        file.extract()
                    except AttributeError:
                        not_extracted.append(file)
                else:
                    not_extracted.append(file)

        return not_extracted

    #def create_dot_vfs(self, target_path) -> str:
    #    with open(target_path, 'wb'):
