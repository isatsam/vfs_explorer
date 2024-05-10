from plaguevfs import VfsArchive
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QStatusBar, QMenu)
from PySide6.QtCore import Qt
from .extractor import Extractor
from .vfs_tree import VfsTree
from .toolbar import UpperToolBar
from .search import Search

STATUSBAR_TIMEOUT = 3500


class UI(QMainWindow):
    def __init__(self, archive):
        super().__init__()

        # calculate and set the window size
        self.window_size = [self.screen().size().width() // 2, self.screen().size().height() // 2]
        self.resize(self.window_size[0], self.window_size[1])

        # create toolbars
        self.mainToolbar = self.createToolbar()
        self.addToolBarBreak()
        self.searchToolbar = self.createSearch()
        self.searchToolbar.hide()

        # create a dummy widget and put the main layout in it
        self.childLayout = QVBoxLayout()
        self.layoutHoldingWidget = QWidget()
        self.layoutHoldingWidget.setLayout(self.childLayout)
        self.setCentralWidget(self.layoutHoldingWidget)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)  # Is set to CustomMenu in createTreeView
        self.customContextMenuRequested.connect(self.callContextMenu)

        # create statusbar
        self.statusBar = self.createStatusBar()

        self.archive = archive

        # generate archive view as a VfsTree (subclass of TreeWidget) and add it to the layout
        if archive:
            self.tree, self.treeItems = self.createTreeView(self.archive)
            self.openFileDialog = None
        else:    # create an "Open archive" button and add it to the layout
            self.createOpenArchiveWindow()
            self.tree, self.treeItems = (None, None)

        self.show()

    def createToolbar(self):
        toolBar = UpperToolBar(self)
        self.addToolBar(toolBar)
        return toolBar

    def createSearch(self):
        searchObj = Search(self)
        searchWidget = searchObj.createSearchWidget()
        '''Search object has bigger control over the general UI than others,
        so its creation is entirely controlled by .createSearchWidget()
        method, including adding itself to the UI. Also, we might want to
        change its widget type later on.'''
        return searchWidget

    def createStatusBar(self):
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        return statusBar

    def createOpenArchiveWindow(self):
        def open_from_file():
            openDialog.exec()
            try:
                selected = openDialog.selectedFiles()[0]
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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        new_vfs_tree = VfsTree(archive)
        all_items_in_tree = get_all_items(new_vfs_tree)

        for widget_index in range(self.childLayout.count()):
            widget = self.childLayout.itemAt(widget_index).widget()
            self.childLayout.removeWidget(widget)

        self.childLayout.addWidget(new_vfs_tree)
        self.statusBar.showMessage(f'Opened {archive.name} containing {len(all_items_in_tree)} files',
                                   STATUSBAR_TIMEOUT)

        return new_vfs_tree, all_items_in_tree

    def callContextMenu(self, point):
        menu = QMenu()
        if len(self.tree.selectedItems()) == 1 and self.tree.selectedItems()[0].childCount() > 0:
            extract_action = menu.addAction("&Extract whole directory")
        else:
            extract_action = menu.addAction("&Extract selected")
        menu.addSeparator()
        unselect_action = menu.addAction("&Clear selection")
        action = menu.exec_(self.mapToGlobal(point))
        if action == extract_action:
            self.extractSelectedFiles()
        elif action == unselect_action:
            self.tree.clearSelection()
        else:
            pass

    def extractSelectedFiles(self):
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

        extracted_files, extracted_to_path = Extractor.extractSelected(extract_files=extract_files,
                                                                       archive=self.archive,
                                                                       parent_obj=self)

        # putting together a statusbar message, based on things .extractSelected() communicated back to us
        msg = f'Extracted to {extracted_to_path}: '
        for i in range(0, min(3, len(extracted_files))):
            text = extracted_files[i]
            print('175: ', text)
            msg += f' {text}'
            if i != min(3, len(extracted_files))-1:
                msg += ','
        if len(extracted_files) > 3:
            msg += f' and {len(extracted_files)-3} more'
        self.statusBar.showMessage(msg, STATUSBAR_TIMEOUT)
