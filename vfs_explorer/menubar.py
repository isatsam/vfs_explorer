import os
from PySide6.QtWidgets import QAbstractButton, QMenu, QMenuBar, QMessageBox, QDialog, QLabel, QStyle, QVBoxLayout, QPushButton
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtCore import QTime, QTranslator, Qt
from .extractor import Extractor
from .updater import Updater
from .config import Global
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
        menu = QMenu(self.tr("&Extract..."))
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

    def setLanguage(self, lang_file):
        Global.settings.setValue("user_language", lang_file)

        # Reinstalling the translator will make all next new windows
        # use the new language (incl. the "restart app..." text)
        Global.app.removeTranslator(Global.translator)
        Global.translator.load(lang_file, Global.path_to_languages)
        Global.app.installTranslator(Global.translator)
        msg = QMessageBox()
        msg.setText(self.tr("Restart app to apply changes"))
        msg.exec()

    def createAboutMenu(self):
        updatesOnStartChecked = Global.settings.value("check_for_updates")
        if updatesOnStartChecked == "true":
            updatesOnStartChecked = True
        else:
            updatesOnStartChecked = False

        menu = QMenu(self.tr("&Preferences"))
        languageSubmenu = QMenu(self.tr("&Language"))

        """ Gather all available language files to display them in the menu """
        languages = []
        for file in os.listdir(os.getcwd()):
            if file.endswith('.qm'):
                languages.append(file)

        for lang in languages:
            this_lang = languageSubmenu.addAction(lang[:lang.find('.qm')])
            this_lang.triggered.connect(
                        lambda x=None, lang=lang: self.setLanguage(lang))
        menu.addMenu(languageSubmenu)

        menu.addSeparator()
        checkForUpdatesOnStart = menu.addAction(
                                    self.tr("&Check for updates on startup"))  # TODO
        checkForUpdatesOnStart.setCheckable(True)
        checkForUpdatesOnStart.setChecked(updatesOnStartChecked)
        checkForUpdatesOnStart.triggered.connect(lambda x=None, checkbox=checkForUpdatesOnStart: self.setCheckingUpdatesOnStart(checkbox))

        checkForUpdates = menu.addAction(self.tr("&Check for updates now"))
        checkForUpdates.triggered.connect(self.checkForUpdates)

        menu.addSeparator()
        showDebugOptionsCheckbox = menu.addAction(
                                            self.tr("&Show debug options"))  # TODO
        showDebugOptionsCheckbox.setCheckable(True)

        menu.addSeparator()
        about = menu.addAction(self.tr("&About VFS Explorer"))
        about.triggered.connect(self.showAboutMenu)
        github = menu.addAction(self.tr("View on GitHub"))
        github.triggered.connect(self.openGithub)

        return menu

    def showAboutMenu(self):
        about = self.tr("""VFS Explorer is a program for viewing and extracting the contents of VFS archives, such as those found in some of the games by Ice-Pick Lodge.
VFS Explorer is licensed under GNU General Public License v3.0, a copy of which is included.
Version: {}""").format(__version__)

        about_menu = QMessageBox()
        about_menu.setText(about)
        about_menu.setWindowTitle(self.tr("About VFS Explorer"))
        about_menu.exec()

    def checkForUpdates(self):
        updater = Updater(self, self.parent())
        updater.checkForUpdates()

    def setCheckingUpdatesOnStart(self, checkbox):
        Global.settings.setValue("check_for_updates", checkbox.isChecked())


    def openGithub(self):
        url = "https://github.com/isatsam/vfs_explorer"
        QDesktopServices.openUrl(url)
