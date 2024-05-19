import sys
import vfs_explorer

if len(sys.argv) > 1:
    vfs_explorer.start(sys.argv[1])
else:
    vfs_explorer.start()
