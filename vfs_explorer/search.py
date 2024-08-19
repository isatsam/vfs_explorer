from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QRadioButton, QToolBar, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
import re
import time


class Search(QLineEdit):
    def __init__(self, parent_obj, mode="contains"):
        self.parent = parent_obj
        super().__init__()

        self.mode = mode
        self.modes = ["contains", "starts with", "regex"]

        self.setPlaceholderText(self.tr("Enter filename..."))
        self.textChanged.connect(self.showSearchResults)

        self.searchWidget = SearchWidget(self)
        self.searchWidget.hide()

    def showSearchResults(self, query):
        query = query.lower()

        found = []
        for item in self.parent.treeItems:
            item.setHidden(True)

        # The following search could probably be optimised but it is also
        # already fairly fast, so...
        if self.mode == "contains":
            for item in self.parent.treeItems:
                if query in item.text(0).lower():
                    found.append(item)
        elif self.mode == "starts with":
            for item in self.parent.treeItems:
                if item.text(0).lower()[:len(query)] == query:
                    found.append(item)
        elif self.mode == "regex":
            query = "(" + query + ")"
            for item in self.parent.treeItems:
                try:
                    match = re.search(query, item.text(0).lower())
                    if match:
                        found.append(item)
                except:
                    pass        # silence re.error exceptions

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
        self.searchBar = searchBar
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.setFloatable(False)
        self.setMovable(False)

        # create buttons for all available search modes dynamically
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        for mode in self.searchBar.modes:
            new_button = QRadioButton(mode.capitalize(), self)
            new_button.clicked.connect(lambda x=None,
                name=mode: self.changeSearchMode(name))
            if mode == "contains":
                new_button.setChecked(True)  # default option
            buttons_layout.addWidget(new_button)

        buttons = QWidget()
        buttons.setLayout(buttons_layout)

        layout = QVBoxLayout()
        layout.addWidget(searchBar)
        layout.addWidget(buttons)
        cont = QWidget()
        cont.setLayout(layout)
        self.addWidget(cont)

    def changeSearchMode(self, new_mode):
        print(f"Using \"{new_mode}\" search mode")
        self.searchBar.mode = new_mode
