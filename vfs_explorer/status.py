from PySide6.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self):
        self.timeout = 10000
        super().__init__()

    def showMessage(self, text, timeout=0):
        if timeout == 0:
            timeout = self.timeout
        super().showMessage(text, timeout)

    def createExtractedMessage(self, extracted_to_path, extracted_files):
        # putting together a statusbar message, based on things .extractSelected() communicated back to us
        msg = self.tr('Extracted to {0}: ').format(extracted_to_path)
        for i in range(0, min(2, len(extracted_files))):
            text = extracted_files[i]
            msg += f' {text}'
            if i != min(3, len(extracted_files))-1:
                msg += ','
        if len(extracted_files) > 3:
            msg += f' and {len(extracted_files)-2} more'
        self.showMessage(msg)
