from PyQt6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem, QHeaderView, QToolBar
import plaguevfs as pvfs
from datetime import datetime

TIME_FORMAT = '%d/%m/%Y, %H:%M:%S'


class VfsTree(QTreeWidget):
    def __init__(self, archive):
        super().__init__()
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.selected = self.selectedItems()
        self.CreateArchiveTreeView(archive)

    def test_action(self, item):
        pass

    def CreateArchiveTreeView(self, archive):
        def add_dir_to_tree(items_list, directory: pvfs.Directory):
            entry = QTreeWidgetItem([directory.name])
            for subdir in directory.subdirs:
                entry.addChildren(add_dir_to_tree(items_list, subdir))
            for file in directory.files.values():
                time = file.timestamp
                time = datetime.fromtimestamp(time).strftime(TIME_FORMAT)

                size = file.length
                if size > 1000000:
                    size = str(size / 1000000)
                    unitname = 'Mb'
                    decimals = 3
                elif size > 1000:
                    size = str(size / 1000)
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

        self.setColumnCount(1)
        header_labels = ["File", "Size", "Last modified"]
        self.setColumnWidth(0, self.window().size().width() // 2)
        self.setHeaderLabels(header_labels)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        items = []
        items = add_dir_to_tree(items, archive.root)
        self.insertTopLevelItems(0, items)


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VFS Manager')

    def createToolbar(self):
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

    def CreateUI(self, archive):
        screen_size = self.screen().size()
        window_size = [screen_size.width() // 2, screen_size.height() // 2]
        self.resize(window_size[0], window_size[1])
        self.setWindowTitle(archive.name)

        self.createToolbar()

        new_vfs_tree = VfsTree(archive)
        self.setCentralWidget(new_vfs_tree)

        self.show()
