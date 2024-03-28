import os
from plaguevfs import VfsArchive
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolBar, QLineEdit, QPushButton, QFileDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from .vfs_tree import VfsTree


class UI(QMainWindow):
    def __init__(self, archive):
        super().__init__()

        self.window_size = [self.screen().size().width() // 2, self.screen().size().height() // 2]
        self.resize(self.window_size[0], self.window_size[1])

        self.mainToolbar = self.createToolbar()
        self.addToolBarBreak()
        self.searchToolbar = self.createSearchBar()

        self.childLayout = QVBoxLayout()
        self.layoutHoldingWidget = QWidget()
        self.layoutHoldingWidget.setLayout(self.childLayout)
        self.setCentralWidget(self.layoutHoldingWidget)

        self.archive = archive
        if archive:
            self.tree, self.treeItems = self.createTreeView(self.archive)
            self.openFileDialog = None
        else:
            self.createOpenArchiveWindow()
            self.tree, self.treeItems = (None, None)

        self.show()

    def createToolbar(self):
        toolbar = QToolBar()
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)

        buttonAction = QAction("Extract selected files", self)
        buttonAction.triggered.connect(self.extractSelected)

        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addAction(buttonAction)

        self.addToolBar(toolbar)
        return toolbar

    def createSearchBar(self):
        searchBar = QLineEdit()
        searchBar.setPlaceholderText("Search")
        searchBar.textChanged.connect(self.showSearchResults)

        toolbar = QToolBar()
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addWidget(searchBar)

        self.addToolBar(toolbar)
        return toolbar

    def showSearchResults(self, text):
        found = []
        for item in self.treeItems:
            item.setHidden(True)

        for item in self.treeItems:
            if text.lower() in item.text(0).lower():
                found.append(item)

        for item in found:
            item.setHidden(False)
            next_parent = item.parent()
            while next_parent is not None:
                next_parent.setHidden(False)
                next_parent.setExpanded(True)
                next_parent = next_parent.parent()

    def createOpenArchiveWindow(self):
        def open_from_file():
            openDialog.exec()
            selected = openDialog.selectedFiles()[0]
            try:
                self.archive = VfsArchive(selected)
                self.tree, self.treeItems = self.createTreeView(self.archive)
            except IndexError:
                pass
            except Exception as e:
                print(e)

        self.setWindowTitle('VFS Toolkit')
        self.mainToolbar.setDisabled(True)
        self.searchToolbar.setDisabled(True)

        openArchiveButton = QPushButton('&Open', self)
        openArchiveButton.setText('Open archive')
        openArchiveButton.setMinimumSize(90, 40)

        openDialog = QFileDialog(self)
        openDialog.setFileMode(QFileDialog.ExistingFile)
        openDialog.setViewMode(QFileDialog.Detail)
        openDialog.setNameFilter('VFS archives (*.vfs)')

        openArchiveButton.clicked.connect(open_from_file)

        self.childLayout.addWidget(openArchiveButton, alignment=Qt.AlignCenter)

        return openDialog

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

        self.setWindowTitle(archive.name)
        self.mainToolbar.setDisabled(False)
        self.searchToolbar.setDisabled(False)

        new_vfs_tree = VfsTree(archive)
        all_items_in_tree = get_all_items(new_vfs_tree)

        for widget_index in range(self.childLayout.count()):
            widget = self.childLayout.itemAt(widget_index).widget()
            self.childLayout.removeWidget(widget)

        self.childLayout.addWidget(new_vfs_tree)

        return new_vfs_tree, all_items_in_tree

    def extractSelected(self):
        if len(self.tree.selectedItems()) > 10:
            pass
        # TODO: spawn "Are you sure you want to extract N items?" popup

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
            def verify_path(embed_file, file_tree_item):
                if not embed_file.parent.parent and file_tree_item.parent() == self.treeItems[0]:
                    """ Check for files in top-level directories/trees """
                    return True

                next_tree_parent = file_tree_item.parent()
                next_embed_parent = embed_file.parent
                i = 0
                while next_tree_parent and next_embed_parent:
                    if next_tree_parent.text(0) != next_embed_parent.name:
                        return False
                    else:
                        next_tree_parent = next_tree_parent.parent()
                        next_embed_parent = next_embed_parent.parent

                return True

            candidates = self.archive.root.search(file_entry.text(0)).values()
            for candidate in candidates:
                if verify_path(candidate, file_entry):
                    candidate.extract(create_subdir_on_disk=True)

        # TODO: 'extract right here' and 'extract by path ./xxx/yyy/etc' should be separate options in the GUI
