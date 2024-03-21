import codecs
import struct


class EmbeddedFile:
    def __init__(self, parent):
        self.parent = parent
        (self.name, self.length, self.start, self.end, self.timestamp) = self.read_self(parent.contents)

    @staticmethod
    def read_self(section):
        def read_int(data):
            b = data.read(4)
            return struct.unpack('<i', b)[0]

        filename_len = ord(section.read(1))
        filename = section.read(filename_len)
        length = read_int(section)
        start = read_int(section)
        end = start+length
        timestamp = section.read(8)

        return [filename, length, start, end, timestamp]

    def extract(self):
        self.parent.contents.seek(self.start)
        data = self.parent.contents.read(self.length)

        out = codecs.decode(self.name, encoding=self.parent.encoding, errors='strict')
        with open(out, 'wb') as f:
            f.write(data)
