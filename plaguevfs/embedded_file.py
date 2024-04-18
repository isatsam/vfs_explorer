import codecs
import struct
import os
from datetime import datetime


class EmbeddedFile:
    def __init__(self, parent):
        self.parent = parent
        (self.name, self.length, self.start, self.end, self.timestamp) = self.read_self(parent.contents)

    def __str__(self):
        return self.name

    def read_self(self, section):
        def to_datetime(filetime: int) -> datetime:
            """
            Converts a Windows filetime number to a Python datetime. The new
            datetime object is timezone-naive but is equivalent to tzinfo=utc.

            This function is adapted from winfiletime by jlenclanche:
            https://github.com/jleclanche/winfiletime
            which is released in the Public Domain.
            """

            # Get seconds and remainder in terms of Unix epoch
            EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as filetime
            HUNDREDS_OF_NS = 10000000
            s, ns100 = divmod(filetime - EPOCH_AS_FILETIME, HUNDREDS_OF_NS)
            # Convert to datetime object, with remainder as microseconds.
            return datetime.utcfromtimestamp(s).replace(microsecond=(ns100 // 10))

        filename_len = ord(section.read(1))
        filename = section.read(filename_len).decode(self.parent.encoding)
        length = struct.unpack('<i', section.read(4))[0]
        start = struct.unpack('<i', section.read(4))[0]
        end = start+length
        timestamp = struct.unpack('<q', section.read(8))[0]
        timestamp = int(to_datetime(timestamp).timestamp())

        return [filename, length, start, end, timestamp]

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
