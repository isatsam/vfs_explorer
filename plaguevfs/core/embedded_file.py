import struct
import codecs

class EmbeddedFile:
    def __init__(self, byte_section=None, parent=None):
        if parent:
            self.parent = parent
            (self.filename, self.length, self.start, self.end,  self.timestamp,
             self.file_type, self.file_type_full_name) = self.read_self(parent.contents)
        elif byte_section:
            (self.filename, self.length, self.start, self.end, self.timestamp,
             self.file_type, self.file_type_full_name) = self.read_self(byte_section)

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

        # TODO: Identify file types (DDS, LSH, mesh, etc...)
        original_position = section.tell()
        try:
            section.seek(start)
            signature = section.read(3)
            match signature:
                case b'DDS':
                    file_type = b'DDS'
                    file_type_full_name = 'Image - DirectDraw Surface (DDS)'
                case bytes(b'\xff\xd8\xff'):
                    file_type = b'JPG'
                    file_type_full_name = 'Image - JPEG'
                case bytes(b'\x89\x50\x4E'):
                    # Not the full PNG signature (3 bytes out of 8) but we're being lazy here
                    file_type = b'PNG'
                    file_type_full_name = 'Image - PNG'
                case _:
                    file_type = None
                    file_type_full_name = 'Unknown'
            section.seek(original_position)

            # If nothing else, test for TGA Ver.2, which has the signature at the end of the file
            # info: http://justsolve.archiveteam.org/wiki/TGA#Identification
            if file_type is None:
                original_position = section.tell()
                section.seek(start+length-19)
                signature = section.read(18)
                if b'TRUEVISION-XFILE' in signature:
                    file_type = b'TGA'
                    file_type_full_name = 'Image - TrueVision Graphics Adapter (TGA) Ver. 2'
                section.seek(original_position)
        except Exception as er:
            #print(er)
            file_type = None
            file_type_full_name = 'Unknown'
        return [filename, length, start, end, timestamp, file_type, file_type_full_name]
