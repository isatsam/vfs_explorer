# Entry file for starting VFS Explorer.
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QDataWidgetMapper
from PySide6.QtCore import QLocale, QSettings, QTranslator, QCoreApplication
from plaguevfs import VfsArchive, VfsError
import sys
import os
from .config import Global
from .ui import UI
from .updater import Updater


def start(path_to_archive=None):
    if path_to_archive is None:
        archive = None
    else:
        try:
            archive = VfsArchive(path_to_archive)
        except (VfsError, FileNotFoundError) as er:
            print(f"Error opening VFS archive: {er}")
            quit()

    # Initialize QSettings
    settings = QSettings("isatsam", "VFS Explorer")

    app = QApplication([])

    lang_subdir = os.path.join("vfs_explorer", "languages")
    lang_path_candidates = [
        # 1. /path/to/binary/vfs_explorer/languages (with "VFS Explorer" or "VFS Explorer.exe")
        os.path.join(QCoreApplication.applicationDirPath(), lang_subdir),
        # 2. /path/to/sourcecode/vfs_explorer/languages (with "vfs_explorer.py")
        os.path.join(os.getcwd(), lang_subdir)
    ]
    for path in lang_path_candidates:
        if os.path.exists(path):
            Global.languages = path

    if Global.languages:
        # Set language
        translator = QTranslator(app)
        if settings.value("user_language"):
            # If user previously selected a language
            translator.load(f'{settings.value("user_language")}.qm', Global.languages)
        elif os.path.isfile(os.path.join(LANG_PATH,
                f'{QLocale.system().language().name}.qm')):
            # If a translation corresponding to user's locale is included
            translator.load(f'{QLocale.system().language().name}.qm', os.getcwd())
        else:
            # Fall back to default language
            translator.load('English.qm', LANG_PATH)
        # Additionally, if en.qm is missing, it will just show "non-translated"
        # strings, which are kind of in English anyways.

        app.installTranslator(translator)
        Global.translator = translator

    Global.app = app
    Global.settings = settings

    # default values
    if Global.settings.value("check_for_updates") is None:
        Global.settings.setValue("check_for_updates", True)
    if Global.settings.value("debug_options") is None:
        Global.settings.setValue("debug_options", False)

    mainWindow = UI(archive)
    app.mainWindow = mainWindow

    # Check for updates on startup, if this was set by user
    if Global.settings.value("check_for_updates") == "true":
        updater = Updater(None, app.mainWindow)
        updater.checkForUpdates()

    sys.exit(app.exec())
