from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from base_window import BaseWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ResultWindow(BaseWindow):

    def __init__(self, saved_signals, saved_filter):
        super().__init__('结果展示', 1200, 900)
        self.saved_signals = saved_signals
        self.saved_filter = saved_filter

        # 打印保存的信号和滤波器参数
        print("Saved Signals:", self.saved_signals)
        print("Saved Filter:", self.saved_filter)

        layout = QVBoxLayout()
        self.label = QLabel(f"展示信号与滤波器效果：")
        layout.addWidget(self.label)

        fig, axs = plt.subplots(3, 3, figsize=(10, 8))

        # Example for plotting signals and filter response:
        # Input signal plot
        axs[0, 0].plot([0, 1, 2], [1, 2, 3])
        axs[0, 0].set_title("输入信号-时域")

        # Filter response plot
        axs[0, 1].plot([0, 1, 2], [2, 3, 1])
        axs[0, 1].set_title("滤波器-时域")

        # Output signal plot
        axs[0, 2].plot([0, 1, 2], [1, 1, 2])
        axs[0, 2].set_title("输出信号-时域")

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        button_layout = QHBoxLayout()
        finish_button = QPushButton('完成')
        finish_button.clicked.connect(self.finish)
        button_layout.addStretch(1)
        button_layout.addWidget(finish_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def finish(self):
        self.close()
