from PyQt5.QtWidgets import QWidget

class BaseWindow(QWidget):
    def __init__(self, title, width=800, height=600):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(300, 300, width, height)
        self.setFixedSize(width, height)
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
