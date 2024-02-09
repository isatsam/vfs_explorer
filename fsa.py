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
                print("Not a VFS contents")
                return None
    else:
        print("File doesn't exist")
        return None


if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument('-a', '--archive', action='store')
    parser.add_argument('-s', '--search')
    parser.add_argument('-x', '--extract')
    args = parser.parse_args()

    if args.archive:
        archive = select_archive(args.archive)
        if not args.search and not args.extract:
            print(f"{archive.filepath}\nFiles: {archive.num_files}\nSubdirectories: {archive.num_subdirs}")
            for subdir in archive.subdirs:
                print(f"Files in subdir \"{subdir.name}\": {subdir.num_files}")
    else:
        print('Can\'t do anything without a VFS contents')
        quit()

    if args.search:
        config.search.search(archive, args.search, mode='print')

    if args.extract:
        config.unpack.unpack(archive, args.extract)
