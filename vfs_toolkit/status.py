from PySide6.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self):
        self.timeout = 3500
        super().__init__()

    def showMessage(self, text, timeout=0):
        if timeout == 0:
            timeout = self.timeout
        super().showMessage(text, timeout)

