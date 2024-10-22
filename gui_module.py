from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFormLayout, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QSpinBox, QDoubleSpinBox
import numpy as np
from signal_module import generate_signals
from filter_module import apply_filter
from plot_module import plot_signals

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('欢迎界面')
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        label = QLabel("欢迎使用滤波器展示程序！")
        layout.addWidget(label)

        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        layout.addWidget(next_button)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.signal_window = SignalSelectionWindow()
        self.signal_window.show()

class SignalSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('信号选择')
        self.setGeometry(300, 300, 400, 300)
        layout = QVBoxLayout()

        self.signal_types = []
        self.form_layout = QFormLayout()

        # 添加信号类型选择
        self.signal_combo = QComboBox()
        self.signal_combo.addItems(['正弦波', '方波', '三角波', '锯齿波', '白噪声', '高斯噪声', '脉冲噪声'])
        self.form_layout.addRow("选择信号类型：", self.signal_combo)

        # 参数输入（幅值，频率，等）
        self.amplitude_input = QDoubleSpinBox()
        self.amplitude_input.setRange(0, 10)
        self.amplitude_input.setValue(1)
        self.form_layout.addRow("幅值：", self.amplitude_input)

        self.frequency_input = QSpinBox()
        self.frequency_input.setRange(1, 1000)
        self.frequency_input.setValue(10)
        self.form_layout.addRow("频率：", self.frequency_input)

        layout.addLayout(self.form_layout)

        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        layout.addWidget(next_button)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.filter_window = FilterSelectionWindow()
        self.filter_window.show()

class FilterSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('滤波器选择')
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['低通滤波器', '高通滤波器', '带通滤波器', '带阻滤波器', '巴特沃兹滤波器', '切比雪夫滤波器'])
        layout.addWidget(self.filter_combo)

        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        layout.addWidget(next_button)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.parameter_window = FilterParameterWindow()
        self.parameter_window.show()

class FilterParameterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('滤波器参数设置')
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()

        self.order_input = QSpinBox()
        self.order_input.setRange(1, 10)
        self.order_input.setValue(3)
        layout.addWidget(QLabel("滤波器阶数："))
        layout.addWidget(self.order_input)

        self.cutoff_input = QDoubleSpinBox()
        self.cutoff_input.setRange(0.1, 1000)
        self.cutoff_input.setValue(100)
        layout.addWidget(QLabel("截止频率："))
        layout.addWidget(self.cutoff_input)

        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        layout.addWidget(next_button)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.result_window = ResultWindow()
        self.result_window.show()

class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('结果展示')
        self.setGeometry(300, 300, 600, 400)
        layout = QVBoxLayout()

        # 这里调用信号生成、滤波器应用和绘图模块
        signals = generate_signals()
        filtered_signals = apply_filter(signals)
        plot_signals(signals, filtered_signals)

        done_button = QPushButton('完成')
        done_button.clicked.connect(self.finish)
        layout.addWidget(done_button)

        self.setLayout(layout)

    def finish(self):
        self.close()
