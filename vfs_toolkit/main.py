from PyQt6.QtWidgets import QApplication
from plaguevfs import VfsArchive, VfsError
import ui
import sys


def main(path_to_archive):
    app = QApplication([])

    # Open and create archive
    OPEN_ARCHIVE = path_to_archive
    try:
        archive = VfsArchive(OPEN_ARCHIVE)
    except (VfsError, FileNotFoundError) as er:
        print(f"Error opening VFS archive: {er}")
        quit()

    mainWindow = ui.UI()
    screen_size = mainWindow.screen().size()
    window_size = [screen_size.width()//2, screen_size.height()//2]
    mainWindow = mainWindow.CreateArchiveTreeView(archive, window_size)
    mainWindow.resize(window_size[0], window_size[1])
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv[1])  # Normally supposed to use sys.arvg[0], but it doesn't work in Pycharm for some reason

