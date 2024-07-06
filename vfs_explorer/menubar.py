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
        self.searchButton = QAction(self.tr("Search"), self)
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
        menu = QMenu(self.tr("&File"))
        open_new = menu.addAction(self.tr("&Open..."))
        close_archive = menu.addAction(self.tr("&Close archive"))

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
            # Filter out shortcuts for when the search bar isn't supposed to
            # show (for example when no archive is open)
            pass
        elif bar_zone.isHidden():
            bar_zone.show()
            bar.setFocus()
            self.searchButton.setText(self.tr("Hide search"))
        else:
            bar_zone.hide()
            self.searchButton.setText(self.tr("Search"))

    def createExtractMenu(self):
        menu = QMenu("&Extract...")
        extract_selected = menu.addAction(self.tr("&Extract selected"))
        extract_selected.setDisabled(True)
        unselect_action = menu.addAction(self.tr("&Clear selection"))
        unselect_action.setDisabled(True)

        menu.addSeparator()

        extract_all = menu.addAction(self.tr("&Extract this archive"))
        extract_dry_run = menu.addAction(self.tr("&Extract this archive" +\
                                    "(dry run - won't write files to disk)"))

        extract_selected.triggered.connect(self.extractSelectedFiles)
        extract_all.triggered.connect(self.extractArchive)
        extract_dry_run.triggered.connect(self.extractDryArchive)
        unselect_action.triggered.connect(self.unselectFiles)

        return menu, extract_selected, extract_all, extract_dry_run, unselect_action

    def extractSelectedFiles(self):
        Extractor.extractSelectedFiles(ui_obj=self.parent(), dry_run=False)

    def extractArchive(self):
        extracted_files, extracted_to_path = Extractor.extractFiles(
                                        files=[self.parent().treeItems[0]],
                                        ui_obj=self.parent(), dry_run=False)
        if extracted_files and extracted_to_path:
            self.parent().statusBar.createExtractedMessage(
                                            extracted_files=extracted_files,
                                            extracted_to_path=extracted_to_path)

    def extractDryArchive(self):
        extracted_files, extracted_to_path = Extractor.extractFiles(
                                            files=[self.parent().treeItems[0]],
                                            ui_obj=self.parent(), dry_run=True)
        if extracted_files and extracted_to_path:
            self.parent().statusBar.createExtractedMessage(
                                        extracted_files=extracted_files,
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
        menu = QMenu(self.tr("&Preferences"))
        languageSubmenu = QMenu(self.tr("&Language"))
        english = languageSubmenu.addAction(self.tr("English"))  # TODO: When we actually have language files,
                                                        # we should loop over them and add languages dynamically
        menu.addMenu(languageSubmenu)

        menu.addSeparator()
        shouldCheckForUpdatesCheckbox = menu.addAction(
                                    self.tr("&Check for updates on startup"))  # TODO
        shouldCheckForUpdatesCheckbox.setCheckable(True)

        checkForUpdates = menu.addAction(self.tr("&Check for updates now"))
        checkForUpdates.triggered.connect(self.checkForUpdates)

        menu.addSeparator()
        showDebugOptionsCheckbox = menu.addAction(
                                            self.tr("&Show debug options"))  # TODO
        showDebugOptionsCheckbox.setCheckable(True)

        menu.addSeparator()
        about = menu.addAction(self.tr("&About VFS Explorer"))
        about.triggered.connect(self.showAboutMenu)

        return menu

    def showAboutMenu(self):
        webpage_url = "https://github.com/hypnotiger/vfs_explorer"

        about = self.tr("VFS Explorer is a program for viewing and extracting the contents of VFS archives, "
                 "such as those found in some of the games by Ice-Pick Lodge.<br>"
                 "VFS Explorer is licensed under GNU General Public License v3.0, a copy of which is included.<br>"
                 f'Website: <a href="{0}">{0}</a><br><br>'
                 f"Version: {1}"
                 ).format(webpage_url, __version__)

        about_menu = QMessageBox(text=about)
        about_menu.setWindowTitle(self.tr("About VFS Explorer"))
        about_menu.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        about_menu.exec()

    def checkForUpdates(self):
        """
        Initializes the check (via requests library) and creates all the
        dialogues needed to tell the use about whether there's any updates available.
        """

        """ We expect that any given URL points towards a page for the latest version,
            and that the URL part after the last slash (/) is the latest version's number.
            In this case, Github's /releases/latest will redirect us
            to wherever we need. If the project ever moves to a service with a different URL setup,
            we will just have rework this bit of code."""
        SOURCE = "https://github.com/hypnotiger/vfs_explorer/releases/latest"

        def open_url():
            QDesktopServices.openUrl(SOURCE)

        self.parent().statusBar.showMessage(
                                self.tr("Checking for new versions..."))

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
            update_dialog.setWindowTitle(self.tr("Update VFS Explorer"))
            update_dialog_layout = QVBoxLayout()

            text = QLabel(update_dialog)
            text.setText(self.tr("You're using version {0}, but version {1}"
                                "is available.<br><br>").format(__version__,
                                                                new_version))

            button = QPushButton()
            button.setText(self.tr("Get it from Github"))
            button.clicked.connect(open_url)

            update_dialog_layout.addWidget(text)
            update_dialog_layout.addWidget(button)
            update_dialog.setLayout(update_dialog_layout)
            update_dialog.adjustSize()

            update_dialog.exec()
        else:
            self.parent().statusBar.showMessage("")
            text = self.tr("No new versions available.")
            msg = QMessageBox(text=text)
            msg.setWindowTitle("VFS Explorer")
            msg.exec()

    def getLatestVersion(self, check_url):
        response = requests.get(check_url)
        if response.status_code != 200:
            text = self.tr("Error {0}. If there's an Internet connection,"
                            "please manually check for a new version.")\
                            .format(response.status_code)
            raise requests.ConnectionError(text)

        ver = response.url.split("/").pop()
        return ver
