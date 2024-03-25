from PySide6.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem, QHeaderView, QToolBar, QLineEdit
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import plaguevfs as pvfs
from datetime import datetime

TIME_FORMAT = '%d/%m/%Y, %H:%M:%S'


class VfsTree(QTreeWidget):
    def __init__(self, archive):
        super().__init__()
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.selectionModel().selectionChanged.connect(self.test_action)

        self.CreateArchiveTreeView(archive)

    def test_action(self):
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
    def __init__(self, archive):
        super().__init__()
        self.archive = archive
        self.tree, self.tree_items = self.createTreeView(self.archive)

        self.tree.topLevelItemCount()

        self.toolbar = self.createToolbar()
        self.searchbar = self.createSearchBar()
        self.toolbar.addWidget(self.searchbar)

        self.show()

    def createToolbar(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setMinimumHeight(40)  # TODO
        self.addToolBar(toolbar)
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        button_action = QAction("Extract selected files", self)
        button_action.triggered.connect(self.extractSelected)
        toolbar.addAction(button_action)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        return toolbar

    def createSearchBar(self):
        search_bar = QLineEdit()
        search_bar.textChanged.connect(self.showSearchResults)

        return search_bar

    def showSearchResults(self, text):
        found = []
        for item in self.tree_items:
            if text.lower() not in item.text(0).lower():
                item.setHidden(True)
            else:
                item.setHidden(False)
                found.append(item)
        for item in found:
            if item.parent():
                item.parent().setHidden(False)
                item.parent().setExpanded(True)

    def createTreeView(self, archive):
        def get_subtree_nodes(tree_widget_item):
            """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
            nodes = [tree_widget_item]
            for i in range(tree_widget_item.childCount()):
                nodes.extend(get_subtree_nodes(tree_widget_item.child(i)))
            return nodes

        def get_all_items(tree_widget):
            """Returns all QTreeWidgetItems in the given QTreeWidget."""
            all_items = []
            for i in range(tree_widget.topLevelItemCount()):
                top_item = tree_widget.topLevelItem(i)
                all_items.extend(get_subtree_nodes(top_item))
            return all_items

        screen_size = self.screen().size()
        window_size = [screen_size.width() // 2, screen_size.height() // 2]
        self.resize(window_size[0], window_size[1])
        self.setWindowTitle(archive.name)

        new_vfs_tree = VfsTree(archive)
        #print(new_vfs_tree.topLevelItemCount())
        #all_items_in_tree = []
        all_items_in_tree = get_all_items(new_vfs_tree)

        self.setCentralWidget(new_vfs_tree)

        return new_vfs_tree, all_items_in_tree

    def extractSelected(self):
        extract_files = []
        extract_dirs = []
        for item in self.tree.selectedItems():
            if item.childCount() == 0:
                extract_files.append(item)
            else:
                extract_dirs.append(item)

        for directory in extract_dirs:
            for i in range(directory.childCount()):
                extract_files.append(directory.child(i))

        for file_entry in extract_files:
            candidates = self.archive.root.search(file_entry.text(0)).values()
            for candidate in candidates:
                if file_entry.parent().text(0) == candidate.parent.name:
                    try:
                        candidate.extract(create_subdir_on_disk=True)
                    except FileNotFoundError:
                        print(file_entry.text(0))
        # TODO: 'extract right here' and 'extract by path ./xxx/yyy/etc' should be separate options in the GUI
        # TODO: prompt a confirmation if extracting over X amount of files
