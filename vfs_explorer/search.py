from PySide6.QtWidgets import QLineEdit, QToolBar
from PySide6.QtCore import Qt


class Search(QLineEdit):
    def __init__(self, parent_obj):
        self.parent = parent_obj

        super().__init__()

        self.setPlaceholderText(self.tr("Search"))
        self.textChanged.connect(self.showSearchResults)

        self.searchWidget = SearchWidget(self)
        self.searchWidget.hide()

    def showSearchResults(self, text):
        treeItems = self.parent.treeItems

        found = []
        for item in treeItems:
            item.setHidden(True)

        for item in treeItems:
            if text.lower() in item.text(0).lower():
                found.append(item)

        for item in found:
            item.setHidden(False)
            next_parent = item.parent()
            while next_parent is not None:
                next_parent.setHidden(False)
                next_parent.setExpanded(True)
                next_parent = next_parent.parent()


class SearchWidget(QToolBar):
    def __init__(self, searchBar):
        super().__init__()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.setFloatable(False)
        self.setMovable(False)
        self.addWidget(searchBar)
