import os
import argparse as arg
import config
from vfs import Vfs


def select_archive(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as file:
            if file.read(4) == b'LP1C':
                vfs = Vfs(filepath)
                return vfs
            else:
                raise TypeError("Not a VFS contents")
    else:
        raise FileNotFoundError("File doesn't exist")


if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument('-a', '--archive', action='store')
    parser.add_argument('-s', '--search')
    parser.add_argument('-x', '--extract')
    args = parser.parse_args()

    if args.archive:
        try:
            archive = select_archive(args.archive)
        except (TypeError, FileNotFoundError) as er:
            print(f"Error opening VFS archive: {er}")
            quit()

        if not args.search and not args.extract:
            print(f"{archive.filepath}\nFiles: {archive.num_files}\nSubdirectories: {archive.num_subdirs}")
            for subdir in archive.subdirs:
                print(f"Files in subdir \"{subdir.name}\": {subdir.num_files}")
    else:
        print('Can\'t do anything without a VFS contents')
        quit()

    if args.search:
        results = config.search.search(archive, args.search)
        for file in results:
            print(f"{file[0]}")

    if args.extract:
        config.unpack.unpack(archive, args.extract)
