import argparse as arg
from core import config
from core.vfs import Vfs
from core.vfs_error import VfsError


if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument('-a', '--archive', action='store')
    parser.add_argument('-s', '--search')
    parser.add_argument('-x', '--extract')
    args = parser.parse_args()

    if args.archive:
        try:
            archive = Vfs(args.archive)
        except (VfsError, FileNotFoundError) as er:
            print(f"Error opening VFS archive: {er}")
            quit()

        if not args.search and not args.extract:
            print(f"{archive.filepath}\nFiles: {archive.num_files}\nSubdirectories: {archive.num_subdirs}")
            for subdir in archive.subdirs:
                print(f"Files in subdir \"{subdir.name}\": {subdir.num_files}")
    else:
        print('Can\'t do anything without a VFS archive')
        quit()

    if args.search:
        results = config.search.search(archive, args.search)
        for file in results:
            print(f"{file[0]}     type: {file[1].file_type}")

    if args.extract:
        config.unpack.unpack(archive, args.extract)
