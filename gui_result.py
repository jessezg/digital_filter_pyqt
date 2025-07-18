from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox
from gui_base import BaseWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from module_plot import plot_signals, generate_convolved_output
from module_filter import apply_filter, filter_func
from module_signal import generate_signals
import numpy as np
from scipy import signal

class ResultWindow(BaseWindow):
    def __init__(self, saved_signals, saved_filter, sample_rate=1000):
        super().__init__('结果展示', 1200, 900)
        self.saved_signals = saved_signals
        self.saved_filter = saved_filter
        self.sample_rate = sample_rate

        # 打印保存的信号和滤波器参数
        # print("Saved Signals:", self.saved_signals)
        # print("Saved Filter:", self.saved_filter)

        layout = QVBoxLayout()
        self.label = QLabel(f"展示信号与滤波器效果：")
        layout.addWidget(self.label)

        # 生成信号
        input_signal = generate_signals(self.saved_signals, self.sample_rate)

        # 应用滤波器
        filter_response = filter_func(self.saved_filter, self.sample_rate)

        # 生成输出
        output_signal = apply_filter(input_signal, self.saved_filter, self.sample_rate)

        # 绘制结果
        fig, axs = plot_signals(input_signal, filter_response, output_signal, self.sample_rate)
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # 完成按钮
        button_layout = QHBoxLayout()
        finish_button = QPushButton('完成')
        finish_button.clicked.connect(self.finish)
        button_layout.addStretch(1)
        button_layout.addWidget(finish_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        
        filter_fft = np.fft.fft(filter_response)
        if max(filter_fft) > 3:
            QMessageBox.warning(self, "图形错误",\
            "阶数过高、下上截止频率过小过大或过于接近，导致 Python 计算精度不足，滤波器频率响应无法实现归一化")

    def finish(self):
        self.close()
