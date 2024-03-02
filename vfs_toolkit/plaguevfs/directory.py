import os


class Directory:
    def __init__(self, name, parent, num_files, num_subdirs, contents):
        self.name = name
        self.parent = parent
        self.num_files = num_files
        self.files = []
        self.files_by_names = []
        self.num_subdirs = num_subdirs
        self.subdirs = []
        self.encoding = 'iso8859-1'
        self.contents = contents

    def make_target_dir(self):
        target_dir = self.name
        try:
            os.mkdir(f"./{target_dir}")
            return target_dir
        except FileExistsError:
            return target_dir
        except PermissionError:
            raise PermissionError('Insufficient permissions to create a directory here')
