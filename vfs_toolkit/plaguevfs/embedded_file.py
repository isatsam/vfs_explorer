import struct


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
        section.seek(start)

        """
        Some files have proper signatures (DDS, PNG, JPG...), in which case we can simply
        look for that signature in the beginning.
        Some other files seem to have no signature (LSH), but have a more-or-less repeating pattern in
        the beginning, in which case we're probably to just use that as a fake 'signature'.
        TGA is a disgusting format that only comes with a signature since Version 2, and that signature
        is placed in the *last* 19 bytes of the file, therefore we have to check for TGA separately.
        
        Some of Pathologic's own file formats (.mesh, actors) apparently don't have a signature, or a reliable
        pattern that could be compared in the beginning of the file. We will either have to hack something together
        to recognise these files by indirect signs, or, the lazy way, to naively rely on the file extension.
        """
        signature = section.read(16)
        if b'DDS' in signature:
            file_type = b'DDS'
            file_type_full_name = 'Image - DirectDraw Surface (DDS)'
        elif b'\xff\xd8\xff' in signature:
            file_type = b'JPG'
            file_type_full_name = 'Image - JPEG'
        elif b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A' in signature:
            file_type = b'PNG'
            file_type_full_name = 'Image - PNG'
        elif b'\x00\x00\xDC\x12\x00\x3F\x54\xE5\xF1\xBE' in signature:
            file_type = b'LSH'
            file_type_full_name = 'LifeStudio:Head Facial Animations'
        else:
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

        return [filename, length, start, end, timestamp, file_type, file_type_full_name]
