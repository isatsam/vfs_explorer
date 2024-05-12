from plaguevfs import VfsArchive
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMenu)
from PySide6.QtCore import Qt
from .extractor import Extractor
from .vfs_tree import VfsTree
from .menubar import MenuBar
from .search import Search


class UI(QMainWindow):
    def __init__(self, archive):
        super().__init__()

        # calculate and set the window size
        self.window_size = [self.screen().size().width() // 2, self.screen().size().height() // 2]
        self.resize(self.window_size[0], self.window_size[1])

        # create toolbars
        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)
        self.addToolBarBreak()
        self.searchToolBar = Search(self).searchWidget
        self.addToolBar(self.searchToolBar)

        # create a dummy widget and put the main layout in it
        self.childLayout = QVBoxLayout()
        self.layoutHoldingWidget = QWidget()
        self.layoutHoldingWidget.setLayout(self.childLayout)
        self.setCentralWidget(self.layoutHoldingWidget)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)  # Is set to CustomMenu in createTreeView
        self.customContextMenuRequested.connect(self.callContextMenu)

        # create statusbar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.archive = archive

        # generate archive view as a VfsTree (subclass of TreeWidget) and add it to the layout
        if archive:
            self.tree, self.treeItems = self.createTreeView(self.archive)
            self.openFileDialog = None
        else:    # create an "Open archive" button and add it to the layout
            self.createEmptyWindow()
            self.tree, self.treeItems = (None, None)

        self.show()

    def setUiDisabled(self, locked: bool):
        if type(locked) is not bool:
            raise TypeError
        self.menuBar.setDisabled(locked)
        self.searchToolBar.setDisabled(locked)

    def openFromFile(self):
        openDialog = QFileDialog(self)
        openDialog.setFileMode(QFileDialog.ExistingFile)
        openDialog.setNameFilter('VFS archives (*.vfs)')
        openDialog.exec()
        try:
            selected = openDialog.selectedFiles()[0]
            self.archive = VfsArchive(selected)
            self.tree, self.treeItems = self.createTreeView(self.archive)
        except IndexError:
            pass
        except Exception as e:
            print(e)

        return openDialog

    def createEmptyWindow(self):
        self.setWindowTitle('VFS Toolkit')
        self.setUiDisabled(True)

        openArchiveButton = QPushButton('&Open', self)
        openArchiveButton.setText('Open archive')
        openArchiveButton.setMinimumSize(90, 40)

        openDialog = openArchiveButton.clicked.connect(self.openFromFile)

        self.childLayout.addWidget(openArchiveButton, alignment=Qt.AlignCenter)

        return openDialog

    def clearLayout(self, layout):
        if layout is not None:
            while self.childLayout.count():
                item = self.childLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

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
        self.setUiDisabled(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        new_vfs_tree = VfsTree(archive)
        all_items_in_tree = get_all_items(new_vfs_tree)

        for widget_index in range(self.childLayout.count()):
            widget = self.childLayout.itemAt(widget_index).widget()
            self.childLayout.removeWidget(widget)

        self.childLayout.addWidget(new_vfs_tree)
        self.statusBar.showMessage(f'Opened {archive.name} containing {len(all_items_in_tree)} files')

        new_vfs_tree.selectionModel().selectionChanged.connect(self.menuBar.toggleExtractSelected)

        return new_vfs_tree, all_items_in_tree

    def callContextMenu(self, point):
        menu = QMenu()
        if len(self.tree.selectedItems()) == 1 and self.tree.selectedItems()[0].childCount() > 0:
            extract_action = menu.addAction("&Extract whole directory")
        else:
            extract_action = menu.addAction("&Extract selected")
        extract_dummy = menu.addAction("&Extract a dry run (won't write files to disk)")
        menu.addSeparator()
        unselect_action = menu.addAction("&Clear selection")
        action = menu.exec_(self.mapToGlobal(point))
        if action == extract_action:
            self.passSelectedFilesToExtractor()
        elif action == extract_dummy:
            self.passSelectedFilesToExtractor(dry_run=True)
        elif action == unselect_action:
            self.tree.clearSelection()
        else:
            pass

    def passSelectedFilesToExtractor(self, dry_run=False):
        extracted_files, extracted_to_path = Extractor.extractSelectedFiles(self, dry_run)

        # putting together a statusbar message, based on things .extractSelected() communicated back to us
        msg = f'Extracted to {extracted_to_path}: '
        for i in range(0, min(3, len(extracted_files))):
            text = extracted_files[i]
            msg += f' {text}'
            if i != min(3, len(extracted_files))-1:
                msg += ','
        if len(extracted_files) > 3:
            msg += f' and {len(extracted_files)-3} more'
        self.statusBar.showMessage(msg, timeout=3500)
