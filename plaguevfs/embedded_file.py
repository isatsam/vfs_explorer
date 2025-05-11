import codecs
import struct
import os
from datetime import datetime


class EmbeddedFile:
    def __init__(self, parent):
        self.parent = parent
        (self.name, self.length, self.start, self.end) = self.read_self(parent.contents)

    def __str__(self):
        return self.name

    def read_self(self, section):
        print("start:", section.tell())
        filename_len = ord(section.read(1))
        section.read(3)
        filename = section.read(filename_len).decode(self.parent.encoding)
        start = struct.unpack('<i', section.read(4))[0]
        length = struct.unpack('<i', section.read(4))[0]
        end = start+length
        print(filename_len, filename, length, start, end)
        return [filename, length, start, end]

    def extract(self, create_subdir_on_disk=False, out_path=os.getcwd()):
        """
        Extracts current file.
        :param create_subdir_on_disk: whether a new subdirectory (named after the file's parent archive)
            should be created for extracting the files. If the directory already exists, will extract to that directory
        :param out_path: path in which the file will be created. If create_subdir_on_disk, the new subdir will be
            created in that path
        :return: nothing
        """
        self.parent.contents.seek(self.start)
        data = self.parent.contents.read(self.length)

        if create_subdir_on_disk:               # if create new subdirectory
            if self.parent.parent and '.' in self.parent.name:
                target_dir = self.parent.name[:self.parent.name.rfind('.')]
            else:
                target_dir = self.parent.name
            out = os.path.join(out_path, target_dir, self.name)
            if not os.path.exists(os.path.join(out_path, target_dir)):
                os.mkdir(os.path.join(out_path, target_dir))
        elif out_path:                          # if extract to specified path
            out = os.path.join(out_path, self.name)
        else:                                   # if no new subdir and no path provided
            out = self.name

        with open(out, 'wb') as f:
            f.write(data)

        dt_epoch = datetime.now().timestamp()
        #      filename   access_date modification_date
        os.utime(out, (dt_epoch, self.timestamp))
