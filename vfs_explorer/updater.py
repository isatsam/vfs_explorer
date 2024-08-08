from enum import CONFORM
import requests
from PySide6.QtWidgets import QAbstractButton, QMenu, QMenuBar, QMessageBox, QDialog, QLabel, QStyle, QVBoxLayout, QPushButton
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtCore import QObject
from .__version__ import __version__


class Updater(QObject):
    def __init__(self, parent_window, main_window) -> None:
        self.parent_window = parent_window
        self.main_window = main_window

    def checkForUpdates(self):
        """
        Initializes the check (via requests library) and creates all the
        dialogues needed to tell the use about whether there's any updates available.
        """

        """ We expect that any given URL points towards a page for the latest version,
            and that the URL part after the last slash (/) is the latest version's number.
            In this case, Github's /releases/latest will redirect us
            to wherever we need. If the project ever moves to a service with a different URL setup,
            we will just have rework this bit of code."""
        SOURCE = "https://github.com/isatsam/vfs_explorer/releases/latest"

        def open_url():
            QDesktopServices.openUrl(SOURCE)

        self.main_window.statusBar.showMessage(self.tr("Checking for new versions..."))
        print("Checking for new versions...")

        try:
            new_version = self.getLatestVersion(SOURCE)
        except requests.ConnectionError as error:
            self.main_window.statusBar.showMessage("")
            text = f"{error}"
            msg = QMessageBox(text=text)
            msg.exec()
            return

        if new_version != __version__:
            update_dialog = QDialog()
            update_dialog.setWindowTitle(self.tr("Update VFS Explorer"))
            update_dialog_layout = QVBoxLayout()

            text = QLabel(update_dialog)
            text.setText(self.tr("You're using version {0}, but version {1} "
                                "is available.<br><br>").format(__version__, new_version))

            button = QPushButton()
            button.setText(self.tr("Get it from Github"))
            button.clicked.connect(open_url)

            update_dialog_layout.addWidget(text)
            update_dialog_layout.addWidget(button)
            update_dialog.setLayout(update_dialog_layout)
            update_dialog.adjustSize()

            update_dialog.exec()
        else:
            self.main_window.statusBar.showMessage("")
            text = self.tr("No new versions available.")
            msg = QMessageBox(text=text)
            msg.setWindowTitle("VFS Explorer")
            msg.exec()

    def getLatestVersion(self, check_url):
        response = requests.get(check_url)
        print(f"Trying to get a new version number from {check_url}")
        if response.status_code != 200:
            text = self.tr("Error {0}. If there's an Internet connection,"
                            "please manually check for a new version.",\
                            ).format(response.status_code)
            print(response.raw)
            raise requests.ConnectionError(text)

        ver = response.url.split("/").pop()
        return ver
