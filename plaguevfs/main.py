from PyQt6.QtWidgets import QApplication
import core.shared as common
from core.vfs import Vfs
from core.vfs_error import VfsError
import ui.ui as ui
import sys

def main():
    app = QApplication([])
    mainWindow = ui.UI()

    # Open and create archive
    OPEN_ARCHIVE = '/home/isa/Projects/plaguevfs/archives/Textures.vfs'
    try:
        archive = Vfs(OPEN_ARCHIVE)
    except (VfsError, FileNotFoundError) as er:
        print(f"Error opening VFS archive: {er}")
        quit()

    if not archive.files:
        common.index.index(archive)
    if not archive.files:
        return []

    print(archive.subdirs[0].files)

    archive_tree = mainWindow.CreateArchiveTreeView(archive)
    archive_tree.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
