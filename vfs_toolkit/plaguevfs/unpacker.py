import codecs
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

        temp_searcher = Searcher()
        file = temp_searcher.search(archive, required)
        if len(file) == 0:
            raise FileNotFoundError(f"{required} not found in contents")

        # TODO: Better handling of multiple results
        # Currently will prompt through cli, otherwise will override
        # file variable with just whatever EmbeddedFile object was found
        # Although on the searcher's level, we could just return only
        # the EmbeddedFile objects, without the name, since they're
        # already aware of its filename
        if type(file) is list:
            if len(file) > 1:
                file = prompt_user_cli(file)
            else:
                file = file[0][1]

        print(file)

        with open(archive.filepath, 'rb') as f:
            f.seek(file.start)
            data = f.read(file.length)

        out = codecs.decode(file.filename, encoding=archive.encoding, errors='strict')
        with open(out, 'wb') as f:
            f.write(data)
