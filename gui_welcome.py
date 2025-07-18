from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from gui_base import BaseWindow
from gui_signal_selection import SignalSelectionWindow

class WelcomeWindow(BaseWindow):
    def __init__(self):
        super().__init__('欢迎界面')
        layout = QVBoxLayout()

        # 增加介绍信息
        label = QLabel(
        """
    欢迎使用滤波器展示程序!
    在这里，你可以创建不同类型的信号，选择滤波器，并观察滤波效果。
    请点击“下一步”开始。
        """
        )
        layout.addWidget(label)

        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.signal_window = SignalSelectionWindow()
        self.signal_window.show()
