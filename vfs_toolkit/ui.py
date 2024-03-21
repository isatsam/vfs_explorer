from PyQt6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem
from datetime import datetime

TIME_FORMAT = '%d/%m/%Y, %H:%M:%S'


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VFS Manager')

    @staticmethod
    def CreateArchiveTreeView(archive, window_size):
        def add_dir_to_tree(items_list, directory):
            entry = QTreeWidgetItem([directory.name])
            for subdir in directory.subdirs:
                entry.addChildren(add_dir_to_tree(items_list, subdir))
            for item in directory.files:
                time = directory.files[item].timestamp
                time = datetime.fromtimestamp(time).strftime(TIME_FORMAT)

                size = directory.files[item].length
                if size > 1000000:
                    size = str(size/1000000)
                    unitname = 'Mb'
                elif size > 1000:
                    size = str(size/1000)
                    unitname = 'Kb'
                else:
                    size = str(size)
                    unitname = 'B'

                # FIXME: this ridiculous decimal precision
                size = str(size[:len(size[:size.rfind('.')]) + 3]) + ' ' + unitname

                child = QTreeWidgetItem([item, size, time])
                entry.addChild(child)
            items_list.append(entry)
            return items_list

        tree = QTreeWidget()
        tree.setColumnCount(1)
        header_labels = ["File", "Size", "Last modified"]
        tree.setHeaderLabels(header_labels)
        tree.setColumnWidth(0, int(window_size[0]*0.5))
        tree.setColumnWidth(1, int(window_size[0]*0.15))
        tree.setColumnWidth(2, int(window_size[0]*0.1))
        items = []
        items = add_dir_to_tree(items, archive.root)
        tree.insertTopLevelItems(0, items)
        return tree

