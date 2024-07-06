# Entry file for starting VFS Explorer.
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLocale, QSettings, QTranslator
from plaguevfs import VfsArchive, VfsError
import sys
import os
from .ui import UI


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

    translator = QTranslator(app)
    if settings.value("user_language"):
        translator.load(f'{settings.value("user_language")}.qm', os.getcwd())
    else:
        translator.load(f'{QLocale.system().name()}.qm', os.getcwd())
    app.installTranslator(translator)

    mainWindow = UI(archive, app)
    sys.exit(app.exec())
