# https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
# 'The canonical way to share information across modules within a single program is to create a special module
# (often called config or cfg). <...> Note that using a module is also the basis for implementing
# the singleton design pattern.'
from indexer import Indexer
from unpacker import Unpacker
from searcher import Searcher

index = Indexer()
unpack = Unpacker()
search = Searcher()
