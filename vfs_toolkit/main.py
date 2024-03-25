from PySide6.QtWidgets import QApplication
from plaguevfs import VfsArchive, VfsError
import sys
from .ui import UI


def main(path_to_archive):
    app = QApplication([])

    # Open and create archive
    OPEN_ARCHIVE = path_to_archive
    try:
        archive = VfsArchive(OPEN_ARCHIVE)
    except (VfsError, FileNotFoundError) as er:
        print(f"Error opening VFS archive: {er}")
        quit()

    mainWindow = UI(archive)

    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv[1])  # Normally supposed to use sys.arvg[0], but it doesn't work in Pycharm for some reason

