from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class UpperToolBar(QToolBar):
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)

        buttonAction = QAction("Extract selected files", self)
        buttonAction.triggered.connect(self.pretendToExtract)

        self.setFloatable(False)
        self.setMovable(False)
        self.addAction(buttonAction)

    @staticmethod
    def pretendToExtract():
        print('Extracted... blah blah')
