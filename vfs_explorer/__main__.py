import sys
from .start import start

if len(sys.argv) > 1:
    start(sys.argv[1])
else:
    start()
