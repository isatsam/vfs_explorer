from PySide6.QtWidgets import QMenu, QMenuBar
from PySide6.QtGui import QAction
from .extractor import Extractor


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.searchButton = QAction("Search", self)
        self.searchButton.triggered.connect(self.showSearchBar)
        self.addAction(self.searchButton)

        (self.extractMenu, self.extractSelected, self.extractAll, self.extractDryRun,
         self.unselectSelected) = self.createExtractMenu()
        self.addMenu(self.extractMenu)

    def toggleExtractSelected(self):
        if self.parent().tree.selectedItems():
            self.extractSelected.setDisabled(False)
            self.unselectSelected.setDisabled(False)
        else:
            self.extractSelected.setDisabled(True)
            self.unselectSelected.setDisabled(True)

    def showSearchBar(self):
        bar = self.parent().searchToolBar
        if bar.isHidden():
            bar.show()
            self.searchButton.setText("Hide search")
        else:
            bar.hide()
            self.searchButton.setText("Search")

    def createExtractMenu(self):
        ui = self.parent()
        menu = QMenu("&Extract...")
        extract_selected = menu.addAction("&Extract selected")
        extract_selected.setDisabled(True)
        unselect_action = menu.addAction("&Clear selection")
        unselect_action.setDisabled(True)

        menu.addSeparator()

        extract_all = menu.addAction("&Extract this archive")
        extract_dry_run = menu.addAction("&Extract this archive (dry run - won't write files to disk)")

        extract_selected.triggered.connect(self.extractSelectedFiles)
        extract_all.triggered.connect(self.extractArchive)
        extract_dry_run.triggered.connect(self.extractDryArchive)

        return menu, extract_selected, extract_all, extract_dry_run, unselect_action

    def extractSelectedFiles(self):
        Extractor.extractSelectedFiles(ui_obj=self.parent(), dry_run=False)

    def extractArchive(self):
        Extractor.extractFiles(files=[self.parent().tree.itemAt(0, 0)], ui_obj=self.parent(), dry_run=False)

    def extractDryArchive(self):
        Extractor.extractFiles(files=[self.parent().tree.itemAt(0, 0)], ui_obj=self.parent(), dry_run=True)
