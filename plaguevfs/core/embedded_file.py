import struct


class EmbeddedFile:
    def __init__(self, byte_section=None, parent=None):
        if parent:
            self.parent = parent
            self.filename, self.length, self.start, self.end, self.file_type = self.read_self(parent.contents)
        elif byte_section:
            self.filename, self.length, self.start, self.end, self.file_type = self.read_self(byte_section)

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
        section.read(8)

        # TODO: Identify file types (DDS, LSH, mesh, etc...)
        file_type = "type"
        return [filename, length, start, end, file_type]
