import codecs
import os
from .vfs import Vfs
from .embedded_file import EmbeddedFile
from .searcher import Searcher


class Unpacker:
    @staticmethod
    def unpack(archive: Vfs, required: str or EmbeddedFile = ""):
        # TODO: Obv not compatible with a GUI but i don't know how to solve this yet
        def prompt_user_cli(files):
            print(f"Select which of the files to extract:")
            num = 0
            for filename in files:
                num += 1
                print(f"{num}. {filename}")
            return files[int(input()) - 1]

        file = []

        if os.path.isfile(required):
            temp_searcher = Searcher()
            file = temp_searcher.search(archive, required, file)
        else:
            raise FileNotFoundError(f"{required} not found in contents")

        if type(file) is list:
            if len(file) > 1:
                file = prompt_user_cli(file)
            elif len(file) == 1:
                file = file[0]

        with open(archive.filepath, 'rb') as f:
            f.seek(file[1].start)
            data = f.read(file[1].length)

        out = codecs.decode(file[1].filename, encoding=archive.encoding, errors='strict')
        with open(out, 'wb') as f:
            f.write(data)