import requests
from PySide6.QtWidgets import QMenu, QMenuBar, QMessageBox, QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtCore import Qt
from .extractor import Extractor
from .__version__ import __version__


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        # Create "File" menu > Open..., Close archive
        self.fileMenu, self.openNew, self.closeThis = self.createFileMenu()
        self.addMenu(self.fileMenu)

        # Create Search button (shows the search bar and focuses on it)
        self.searchButton = QAction("Search", self)
        self.searchButton.triggered.connect(self.showSearchBar)
        self.addAction(self.searchButton)

        # Create Extract menu > all the extract options
        (self.extractMenu, self.extractSelected, self.extractAll, self.extractDryRun,
         self.unselectSelected) = self.createExtractMenu()
        self.addMenu(self.extractMenu)

        # Create About menu > About VFS Explorer, Check for new versions
        self.aboutMenu = self.createAboutMenu()
        self.addMenu(self.aboutMenu)

        self.disableAbleElements = [self.fileMenu, self.searchButton, self.extractMenu]

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
        bar = self.parent().searchLine
        bar_zone = self.parent().searchToolBar

        if not self.searchButton.isEnabled():
            # Filter out shortcuts for when the search bar isn't supposed to show (for example when no archive is open)
            pass
        elif bar_zone.isHidden():
            bar_zone.show()
            bar.setFocus()
            self.searchButton.setText("Hide search")
        else:
            bar_zone.hide()
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
        menu = QMenu("&Preferences")
        about = menu.addAction("&About VFS Explorer")
        menu.addSeparator()
        shouldCheckForUpdatesCheckbox = menu.addAction("&Check for updates on startup")
        shouldCheckForUpdatesCheckbox.setCheckable(True)
        updates = menu.addAction("&Check for updates now")

        about.triggered.connect(self.showAboutMenu)
        updates.triggered.connect(self.checkForUpdates)

        return menu

    @staticmethod
    def showAboutMenu():
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
        about_menu.setWindowTitle("About VFS Explorer")
        about_menu.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        about_menu.exec()

    def checkForUpdates(self):
        """
        Initializes the check (via requests library) and creates all the dialogues needed to tell the user
        about whether there's any updates available.
        """

        """ We expect that any given URL points towards a page for the latest version, 
            and that the URL part after the last slash (/) is the latest version's number. 
            So, essentially, we are only ready for Github's /releases/latest, which will redirect us 
            to wherever we need. If the project ever moves to a service with a different URL setup, 
            we will just have rework a little bit of code."""
        SOURCE = "https://github.com/hypnotiger/vfs_explorer/releases/latest"

        def open_url():
            QDesktopServices.openUrl(SOURCE)

        self.parent().statusBar.showMessage("Checking for new versions...")

        try:
            new_version = self.getLatestVersion(SOURCE)
        except requests.ConnectionError as error:
            self.parent().statusBar.showMessage("")
            text = f"{error}"
            msg = QMessageBox(text=text)
            msg.exec()
            return

        if new_version != __version__:
            update_dialog = QDialog()
            update_dialog.setWindowTitle("Update VFS Explorer")
            update_dialog_layout = QVBoxLayout()

            text = QLabel(update_dialog)
            text.setText(f"You're using version {__version__}, but version {new_version} is available.<br><br>")

            button = QPushButton()
            button.setText("Get it from Github")
            button.clicked.connect(open_url)

            update_dialog_layout.addWidget(text)
            update_dialog_layout.addWidget(button)

            update_dialog.setLayout(update_dialog_layout)

            update_dialog.adjustSize()

            self.parent().statusBar.showMessage("New version available...")

            update_dialog.exec()
        else:
            self.parent().statusBar.showMessage("")
            text = "No new versions available."
            msg = QMessageBox(
                text=text
            )
            msg.setWindowTitle("VFS Explorer")
            msg.exec()

    @staticmethod
    def getLatestVersion(check_url):
        response = requests.get(check_url)
        if response.status_code != 200:
            raise requests.ConnectionError(f"Error {response.status_code}." +
                                           "If there's an Internet connection, please manually check for a new "
                                           + "version.")

        ver = response.url.split("/").pop()
        return ver
