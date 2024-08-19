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
        self.searchButton = QAction(self.tr("Filter"), self)
        self.searchButton.triggered.connect(self.showSearchBar)
        self.addAction(self.searchButton)

        # Create Extract menu > all the extract options
        self.extractMenu, self.extractSelected, self.unselectSelected = self.createExtractMenu()
        self.debugOptions = self.createDebugOptions()
        if Global.settings.value("debug_options") == "true":
            self.debugOptions.setVisible(True)
        else:
            self.debugOptions.setVisible(False)
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
            self.searchButton.setText(self.tr("Hide filter"))
        else:
            bar_zone.hide()
            self.searchButton.setText(self.tr("Filter"))

    def createExtractMenu(self):
        menu = QMenu(self.tr("&Extract..."))
        extract_selected = menu.addAction(self.tr("&Extract selected"))
        extract_selected.setDisabled(True)
        unselect_action = menu.addAction(self.tr("&Clear selection"))
        unselect_action.setDisabled(True)

        menu.addSeparator()

        extract_all = menu.addAction(self.tr("&Extract this archive"))

        extract_selected.triggered.connect(self.extractSelectedFiles)
        extract_all.triggered.connect(self.extractArchive)
        unselect_action.triggered.connect(self.unselectFiles)

        return menu, extract_selected, unselect_action

    def createDebugOptions(self):
        extract_dry_run = self.extractMenu.addAction(self.tr("&Extract this archive" +\
                                    "(dry run - won't write files to disk)"))
        extract_dry_run.triggered.connect(self.extractDryArchive)
        return extract_dry_run

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
        menu = QMenu(self.tr("&Preferences"))
        languageSubmenu = QMenu(self.tr("&Language"))

        # Gather all available language files to display them in the menu
        languages = []
        for file in os.listdir(Global.path_to_languages):
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
        checkForUpdatesOnStart.triggered.connect(lambda x=None,
            checkbox=checkForUpdatesOnStart: self.setUpdatesOnStart(checkbox))
        if Global.settings.value("check_for_updates") == "true":
            checkForUpdatesOnStart.setChecked(True)

        checkForUpdates = menu.addAction(self.tr("&Check for updates now"))
        checkForUpdates.triggered.connect(self.checkForUpdates)

        menu.addSeparator()
        showDebugOptionsCheckbox = menu.addAction(
                                            self.tr("&Show debug options"))  # TODO
        showDebugOptionsCheckbox.setCheckable(True)
        showDebugOptionsCheckbox.triggered.connect(lambda x=None,
            checkbox=showDebugOptionsCheckbox: self.setDebugOptions(checkbox))
        if Global.settings.value("debug_options") == "true":
            showDebugOptionsCheckbox.setChecked(True)

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

    def setUpdatesOnStart(self, checkbox):
        checkbox = checkbox.isChecked()
        if checkbox:
            Global.settings.setValue("check_for_updates", "true")
        else:
            Global.settings.setValue("check_for_updates", "false")

    def setDebugOptions(self, checkbox):
        checked = checkbox.isChecked()
        if checked:
            Global.settings.setValue("debug_options", "true")
            if not self.debugOptions.isVisible():
                self.debugOptions.setVisible(True)
        else:
            Global.settings.setValue("debug_options", "false")
            if self.debugOptions.isVisible():
                self.debugOptions.setVisible(False)

    def openGithub(self):
        url = "https://github.com/isatsam/vfs_explorer"
        QDesktopServices.openUrl(url)
