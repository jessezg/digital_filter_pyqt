from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFormLayout, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QSpinBox, QDoubleSpinBox, QScrollArea
from PyQt5.QtCore import Qt
import numpy as np
from signal_module import generate_signals
from filter_module import apply_filter
from plot_module import plot_signals

class BaseWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 600, 400)
        self.setFixedSize(600, 400)
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class WelcomeWindow(BaseWindow):
    def __init__(self):
        super().__init__('欢迎界面')
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

class SignalSelectionWindow(BaseWindow):
    def __init__(self):
        super().__init__('信号选择')
        layout = QVBoxLayout()

        self.signal_entries = []
        self.form_layout = QVBoxLayout()

        # Scrollable area to accommodate dynamic signal rows
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll_layout.addLayout(self.form_layout)

        add_button = QPushButton('添加信号')
        add_button.clicked.connect(self.add_signal_row)
        layout.addWidget(add_button)

        # 下一个按钮
        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        layout.addWidget(next_button)

        # 上一步按钮
        back_button = QPushButton('上一步')
        back_button.clicked.connect(self.back_window)
        layout.addWidget(back_button)

        layout.addWidget(scroll)
        self.setLayout(layout)

    def add_signal_row(self):
        row_layout = QHBoxLayout()

        signal_combo = QComboBox()
        signal_combo.addItems(['正弦波', '方波', '三角波', '锯齿波', '白噪声', '高斯噪声', '脉冲噪声'])

        amplitude_input = QDoubleSpinBox()
        amplitude_input.setRange(0, 10)
        amplitude_input.setValue(1)

        frequency_input = QSpinBox()
        frequency_input.setRange(1, 1000)
        frequency_input.setValue(10)

        row_layout.addWidget(signal_combo)
        row_layout.addWidget(QLabel("幅值:"))
        row_layout.addWidget(amplitude_input)
        row_layout.addWidget(QLabel("频率:"))
        row_layout.addWidget(frequency_input)

        self.form_layout.addLayout(row_layout)
        self.signal_entries.append((signal_combo, amplitude_input, frequency_input))

    def next_window(self):
        self.close()
        self.filter_window = FilterSelectionWindow()
        self.filter_window.show()

    def back_window(self):
        self.close()
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()

class FilterSelectionWindow(BaseWindow):
    def __init__(self):
        super().__init__('滤波器选择')
        layout = QVBoxLayout()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['低通滤波器', '高通滤波器', '带通滤波器', '带阻滤波器', '巴特沃兹滤波器', '切比雪夫滤波器'])
        self.filter_combo.currentIndexChanged.connect(self.display_filter_params)
        layout.addWidget(self.filter_combo)

        self.param_layout = QFormLayout()

        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        layout.addWidget(next_button)

        back_button = QPushButton('上一步')
        back_button.clicked.connect(self.back_window)
        layout.addWidget(back_button)

        layout.addLayout(self.param_layout)
        self.setLayout(layout)

    def display_filter_params(self):
        self.param_layout = QFormLayout()
        filter_type = self.filter_combo.currentText()

        if filter_type == '低通滤波器' or filter_type == '高通滤波器':
            self.cutoff_input = QDoubleSpinBox()
            self.cutoff_input.setRange(0.1, 1000)
            self.param_layout.addRow("截止频率：", self.cutoff_input)

        elif filter_type == '带通滤波器' or filter_type == '带阻滤波器':
            self.low_cut_input = QDoubleSpinBox()
            self.high_cut_input = QDoubleSpinBox()
            self.low_cut_input.setRange(0.1, 1000)
            self.high_cut_input.setRange(0.1, 1000)
            self.param_layout.addRow("低截止频率：", self.low_cut_input)
            self.param_layout.addRow("高截止频率：", self.high_cut_input)

        elif filter_type == '巴特沃兹滤波器' or filter_type == '切比雪夫滤波器':
            self.cutoff_input = QDoubleSpinBox()
            self.cutoff_input.setRange(0.1, 1000)
            self.order_input = QSpinBox()
            self.order_input.setRange(1, 10)
            self.param_layout.addRow("截止频率：", self.cutoff_input)
            self.param_layout.addRow("滤波器阶数：", self.order_input)

    def next_window(self):
        self.close()
        self.parameter_window = FilterParameterWindow()
        self.parameter_window.show()

    def back_window(self):
        self.close()
        self.signal_window = SignalSelectionWindow()
        self.signal_window.show()

class FilterParameterWindow(BaseWindow):
    def __init__(self):
        super().__init__('滤波器参数设置')
        layout = QVBoxLayout()

        done_button = QPushButton('下一步')
        done_button.clicked.connect(self.next_window)
        layout.addWidget(done_button)

        back_button = QPushButton('上一步')
        back_button.clicked.connect(self.back_window)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.result_window = ResultWindow()
        self.result_window.show()

    def back_window(self):
        self.close()
        self.filter_window = FilterSelectionWindow()
        self.filter_window.show()

class ResultWindow(BaseWindow):
    def __init__(self):
        super().__init__('结果展示')
        layout = QVBoxLayout()

        # 调用信号生成、滤波器应用和绘图模块
        signals = generate_signals()
        filtered_signals = apply_filter(signals)
        plot_signals(signals, filtered_signals)

        done_button = QPushButton('完成')
        done_button.clicked.connect(self.finish)
        layout.addWidget(done_button)

        self.setLayout(layout)

    def finish(self):
        self.close()
