from PyQt6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem, QHeaderView
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
            for file in directory.files.values():
                time = file.timestamp
                time = datetime.fromtimestamp(time).strftime(TIME_FORMAT)

                size = file.length
                if size > 1000000:
                    size = str(size/1000000)
                    unitname = 'Mb'
                    decimals = 3
                elif size > 1000:
                    size = str(size/1000)
                    unitname = 'Kb'
                    decimals = 0
                else:
                    size = str(size)
                    unitname = 'B'
                    decimals = 0

                # FIXME: this ridiculous decimal precision
                size = str(size[:len(size[:size.rfind('.')]) + decimals]) + ' ' + unitname

                child = QTreeWidgetItem([str(file), size, time])
                entry.addChild(child)
            items_list.append(entry)
            return items_list

        tree = QTreeWidget()
        tree.setColumnCount(1)
        header_labels = ["File", "Size", "Last modified"]
        tree.setColumnWidth(0, window_size[0]//2)
        tree.setHeaderLabels(header_labels)
        tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        items = []
        items = add_dir_to_tree(items, archive.root)
        tree.insertTopLevelItems(0, items)
        return tree

