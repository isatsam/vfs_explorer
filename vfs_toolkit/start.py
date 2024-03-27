from PySide6.QtWidgets import QApplication
from plaguevfs import VfsArchive, VfsError
import sys
from .ui import UI


def start(path_to_archive=None):

    if path_to_archive:
        # Create archive from argument passed to QApplication instance
        app = QApplication([path_to_archive])
        try:
            archive = VfsArchive(app.arguments()[0])
        except (VfsError, FileNotFoundError) as er:
            print(f"Error opening VFS archive: {er}")
            quit()

        mainWindow = UI(archive)

    else:
        app = QApplication([])
        mainWindow = UI(None)

    sys.exit(app.exec())
