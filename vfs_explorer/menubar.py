from PySide6.QtWidgets import QMenu, QMenuBar, QMessageBox, QDialog, QLabel, QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from .extractor import Extractor
from .__version__ import __version__


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.fileMenu, self.openNew, self.closeThis = self.createFileMenu()
        self.addMenu(self.fileMenu)

        self.searchButton = QAction("Search", self)
        self.searchButton.triggered.connect(self.showSearchBar)
        self.addAction(self.searchButton)

        (self.extractMenu, self.extractSelected, self.extractAll, self.extractDryRun,
         self.unselectSelected) = self.createExtractMenu()
        self.addMenu(self.extractMenu)

        self.aboutMenu = self.createAboutMenu()
        self.addMenu(self.aboutMenu)

    def createFileMenu(self):
        menu = QMenu("&File")
        open_new = menu.addAction("&Open...")
        close_archive = menu.addAction("&Close archive")

        open_new.triggered.connect(self.openNewAction)
        close_archive.triggered.connect(self.closeArchiveAction)

        return menu, open_new, close_archive

    def openNewAction(self):
        self.parent().openFromFile()

    def closeArchiveAction(self):
        self.parent().clearLayout(self.parent().childLayout)
        self.parent().createEmptyWindow()

    def showSearchBar(self):
        bar = self.parent().searchToolBar
        if bar.isHidden():
            bar.show()
            self.searchButton.setText("Hide search")
        else:
            bar.hide()
            self.searchButton.setText("Search")

    def createExtractMenu(self):
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
        unselect_action.triggered.connect(self.unselectFiles)

        return menu, extract_selected, extract_all, extract_dry_run, unselect_action

    def extractSelectedFiles(self):
        Extractor.extractSelectedFiles(ui_obj=self.parent(), dry_run=False)

    def extractArchive(self):
        extracted_files, extracted_to_path = Extractor.extractFiles(files=[self.parent().treeItems[0]],
                                                                    ui_obj=self.parent(), dry_run=False)
        if extracted_files and extracted_to_path:
            self.parent().statusBar.createExtractedMessage(extracted_files=extracted_files,
                                                           extracted_to_path=extracted_to_path)

    def extractDryArchive(self):
        extracted_files, extracted_to_path = Extractor.extractFiles(files=[self.parent().treeItems[0]],
                                                                    ui_obj=self.parent(), dry_run=True)
        if extracted_files and extracted_to_path:
            self.parent().statusBar.createExtractedMessage(extracted_files=extracted_files,
                                                           extracted_to_path=extracted_to_path)

    def unselectFiles(self):
        self.parent().tree.clearSelection()

    def toggleExtractSelected(self):
        if self.parent().tree.selectedItems():
            self.extractSelected.setDisabled(False)
            self.unselectSelected.setDisabled(False)
        else:
            self.extractSelected.setDisabled(True)
            self.unselectSelected.setDisabled(True)

    def createAboutMenu(self):
        menu = QMenu("&Help")
        about = menu.addAction("&About VFS Explorer")

        about.triggered.connect(self.showAboutMenu)

        return menu

    def showAboutMenu(self, product_version):
        webpage_url = "https://github.com/hypnotiger/vfs_explorer"

        about = ("VFS Explorer is a program for viewing and extracting the contents of VFS archives, "
                 "such as those found in some of the games by Ice-Pick Lodge.<br>"
                 "VFS Explorer is licensed under GNU General Public License v3.0, a copy of which is included.<br>"
                 f'Website: <a href="{webpage_url}">{webpage_url}</a><br><br>'
                 f"Version: {__version__}"
                 )

        about_menu = QMessageBox(
            text=about
        )
        about_menu.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        about_menu.exec()
