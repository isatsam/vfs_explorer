# Entry file for starting VFS Explorer.
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QDataWidgetMapper
from PySide6.QtCore import QLocale, QSettings, QTranslator
from plaguevfs import VfsArchive, VfsError
import sys
import os
from .ui import UI
from .config import Global


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
        # If user previously selected a language
        translator.load(f'{settings.value("user_language")}.qm', os.getcwd())
    elif os.path.isfile(os.path.join(f'{QLocale.system().language().name}.qm',
                                                                os.getcwd())):
        # If a translation corresponding to user's locale is included
        translator.load(f'{QLocale.system().language().name}.qm.', os.getcwd())
    else:
        # Fall back to default language
        translator.load('English.qm', os.getcwd())
    # Additionally, if en.qm is missing, it will just show "non-translated"
    # strings, which are kind of in English anyways.

    app.installTranslator(translator)

    mainWindow = UI(archive)
    app.mainWindow = mainWindow

    Global.app = app
    Global.translator = translator
    Global.settings = settings

    sys.exit(app.exec())
