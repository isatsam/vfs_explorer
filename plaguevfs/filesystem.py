from .directory import Directory


class Filesystem:
    def __init__(self, name: str, root: Directory, filepath: str = None):
        self.name = name
        self.root = root
        self.filepath = filepath

    #def create_dot_vfs(self, target_path) -> str:
    #    with open(target_path, 'wb'):
