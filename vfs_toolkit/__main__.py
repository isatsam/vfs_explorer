import sys
from .start import start

try:
    start(sys.argv[1])
except IndexError:
    print('Specify path to or filename of a VFS archive, like so:')
    print('   python3 -m vfs_toolkit Example.vfs')
    