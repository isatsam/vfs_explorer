import argparse as arg
from plaguevfs import Vfs, VfsError


if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument('-a', '--archive', action='store')
    parser.add_argument('-s', '--search')
    parser.add_argument('-x', '--extract')
    parser.add_argument('--extract_all', action='store_true')
    args = parser.parse_args()

    if args.archive:
        try:
            archive = Vfs(args.archive)
        except (VfsError, FileNotFoundError) as er:
            print(f"Error opening VFS archive: {er}")
            quit()

        if not args.search and not args.extract and not args.extract_all:
            print(f"{archive.filepath}\nFiles: {archive.num_files}\nSubdirectories: {archive.num_subdirs}")
            for subdir in archive.subdirs:
                print(f"Files in subdir \"{subdir.name}\": {subdir.num_files}")
    else:
        print('Can\'t do anything without a VFS archive')
        quit()

    if args.extract_all:
        archive.unpack()
        print(f'Extracted {archive.name}')

    if args.search:
        results = archive.search(args.search)
        for file in results:
            print(f"{file} in {results[file].parent.name}")

    if args.extract:
        results = archive.search(args.extract)
        if len(results) == 1:
            item = results[list(results.keys())[0]][1]
            item.extract()
            print(f'Extracted {item.name.decode(item.parent.encoding)}')
        else:
            print("Select which file to extract:\n")
            i = 0
            for result in results:
                print(f"{i}. {result}")
                i += 1
            selected = int(input('\n'))
            if selected < len(results):
                item = results[list(results.keys())[selected]]
                item.extract()
                print(f'Extracted {item.name.decode(item.parent.encoding)}')
            else:
                quit()
