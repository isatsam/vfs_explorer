from PyQt6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem
import codecs
from plaguevfs.core.subdirectory import Subdirectory


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VFS Manager')

    @staticmethod
    def CreateArchiveTreeView(archive):
        def add_dir_to_tree(items_list, directory):
            entry = QTreeWidgetItem([directory.name])
            for subdir in directory.subdirs:
                entry.addChildren(add_dir_to_tree(items_list, subdir))
            for item in directory.files:
                if type(directory) is Subdirectory:
                    print([codecs.decode(item, directory.encoding)])
                child = QTreeWidgetItem([codecs.decode(item, directory.encoding)])
                entry.addChild(child)
            items_list.append(entry)
            return items_list

        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.setHeaderLabels(["File"])
        items = []
        items = add_dir_to_tree(items, archive)

        tree.insertTopLevelItems(0, items)
        return tree
