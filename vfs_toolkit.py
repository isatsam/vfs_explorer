import sys
import vfs_toolkit

if len(sys.argv) > 1:
    vfs_toolkit.start(sys.argv[1])
else:
    vfs_toolkit.start()
