from PySide6.QtWidgets import QMainWindow, QToolBar, QLineEdit
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from .vfs_tree import VfsTree


class UI(QMainWindow):
    def __init__(self, archive):
        super().__init__()
        self.archive = archive
        self.tree, self.tree_items = self.createTreeView(self.archive)

        self.tree.topLevelItemCount()

        self.createToolbar()
        self.addToolBarBreak()
        self.createSearchBar()

        self.show()

    def createToolbar(self):
        toolbar = QToolBar()
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        button_action = QAction("Extract selected files", self)
        button_action.triggered.connect(self.extractSelected)
        toolbar.addAction(button_action)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        self.addToolBar(toolbar)

    def createSearchBar(self):
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search files")
        search_bar.textChanged.connect(self.showSearchResults)

        toolbar = QToolBar()
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.addWidget(search_bar)

        self.addToolBar(toolbar)

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
            def verify_path(embed_file, file_tree_item):
                if not embed_file.parent.parent and file_tree_item.parent() == self.tree_items[0]:
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
        # TODO: prompt a confirmation if extracting over X amount of files
