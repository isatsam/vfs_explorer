from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QMenu
import plaguevfs as pvfs
from datetime import datetime

TIME_FORMAT = '%d/%m/%Y, %H:%M:%S'


class VfsTree(QTreeWidget):
    def __init__(self, archive):
        super().__init__()
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)

        self.archive = archive
        self.CreateArchiveTreeView(self.archive)
        self.itemAt(0, 0).setExpanded(True)

    def CreateArchiveTreeView(self, archive) -> None:
        def add_dir_to_tree(items_list, directory: pvfs.Directory):
            entry = VfsTreeItemDirectory([directory.name], directory)
            for subdir in directory.subdirs:
                entry.addChildren(add_dir_to_tree(items_list, subdir))
            for file in directory.files.values():
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

                child = VfsTreeItemFile([str(file), size], file)
                entry.addChild(child)
            items_list.append(entry)
            return items_list

        self.setColumnCount(1)
        header_labels = [self.tr("Filename"), self.tr("Size")]
        self.setColumnWidth(0, self.window().size().width() // 2)
        self.setHeaderLabels(header_labels)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        items = []
        items = add_dir_to_tree(items, archive.root)
        self.insertTopLevelItems(0, items)

    def selectedFiles(self) -> list:
        """ :return List containing EmbeddedFiles objects corresponding to self.selectedItems()"""
        files = []
        for item in self.selectedItems():
            if type(item) is VfsTreeItemFile:
                files.append(item)
            elif type(item) is VfsTreeItemDirectory:
                files += item.getEmbeddedFiles()

        return files


class VfsTreeItemFile(QTreeWidgetItem):
    def __init__(self, other, embeddedFile):
        super().__init__(other)
        self.embeddedFile = embeddedFile


class VfsTreeItemDirectory(QTreeWidgetItem):
    def __init__(self, other, directory):
        super().__init__(other)
        self.directory = directory

    def getEmbeddedFiles(self) -> list:
        def iterate(directory):
            new_list = []
            for i in range(directory.childCount()):
                if type(directory.child(i)) is VfsTreeItemDirectory:
                    new_list += iterate(directory.child(i))
                else:
                    new_list.append(directory.child(i).embeddedFile)
            return new_list

        selected = iterate(self)
        return selected
