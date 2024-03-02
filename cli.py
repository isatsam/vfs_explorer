import argparse as arg
from plaguevfs import Vfs, VfsError, Locator


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
            print(f"{file[0]} in {file[1].parent.name}")

    if args.extract:
        results = locator.search(args.extract)
        print(results)
        if len(results) == 1:
            item = results[0][1]
            item.extract()
            print(f'Extracted {item.name.decode(results[i][1].parent.encoding)}')
        else:
            print("Select one of the files:\n")
            for i in range(len(results)):
                print(f"{i}. {results[i][1].parent.name}/{results[i][1].name.decode(results[i][1].parent.encoding)}")
            selected = int(input())
            if selected < len(results):
                item = results[selected][1]
                item.extract()
                print(f'Extracted {item.name.decode(results[i][1].parent.encoding)}')
            else:
                quit()
