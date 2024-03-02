from PyQt6.QtWidgets import QApplication
from plaguevfs import Vfs, VfsError, Indexer
import ui
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
        temp_index = Indexer()
        temp_index.index(archive)
    if not archive.files:
        return []

    mainWindow = ui.UI()
    mainWindow = mainWindow.CreateArchiveTreeView(archive)
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main('/home/isa/Projects/patho_vfs/archives/Textures.vfs')
