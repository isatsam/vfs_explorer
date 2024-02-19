from PyQt6.QtWidgets import QApplication
import core.config as config
from core.vfs import Vfs
from core.vfs_error import VfsError
import ui.ui as ui
import sys


def main(path_to_archive):
    app = QApplication([])

    # Open and create archive
    OPEN_ARCHIVE = path_to_archive
    try:
        archive = Vfs(OPEN_ARCHIVE)
    except (VfsError, FileNotFoundError) as er:
        print(f"Error opening VFS archive: {er}")
        quit()

    if not archive.files:
        config.index.index(archive)
    if not archive.files:
        return []

    mainWindow = ui.UI()
    mainWindow = mainWindow.CreateArchiveTreeView(archive)
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main('/home/isa/Projects/plaguevfs/archives/Textures.vfs')
