from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class UpperToolBar(QToolBar):
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.setFloatable(False)
        self.setMovable(False)

        # buttonAction = QAction("Extract selected files", self)
        # buttonAction.triggered.connect(self.startExtraction)

        self.searchButton = QAction("Show search", self)
        self.searchButton.triggered.connect(self.showSearchBar)
        self.addAction(self.searchButton)

    def showSearchBar(self):
        bar = self.parent().searchToolBar
        if bar.isHidden():
            bar.show()
            self.searchButton.setText("Hide search")
        else:
            bar.hide()
            self.searchButton.setText("Show search")
