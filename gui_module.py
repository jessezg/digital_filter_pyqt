from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFormLayout, QLineEdit, QRadioButton, QButtonGroup
from PyQt5.QtWidgets import QHBoxLayout, QSpinBox, QDoubleSpinBox, QScrollArea, QGroupBox
from PyQt5.QtCore import Qt
import numpy as np
from signal_module import generate_signals
from filter_module import apply_filter
from plot_module import plot_signals

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # 按钮靠右
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def next_window(self):
        self.close()
        self.signal_window = SignalSelectionWindow()
        self.signal_window.show()

class SignalSelectionWindow(BaseWindow):
    def __init__(self, saved_signals=None):
        super().__init__('信号选择')
        self.saved_signals = saved_signals if saved_signals else []
        self.signal_entries = []
        layout = QVBoxLayout()

        self.form_layout = QVBoxLayout()

        signal_list_combo = QComboBox()
        signal_list_combo.addItems(['正弦波', '方波', '三角波', '锯齿波', '白噪声', '高斯噪声', '脉冲噪声'])
        add_signal_button = QPushButton('添加信号')
        add_signal_button.clicked.connect(lambda: self.add_signal_row(signal_list_combo.currentText()))
        layout.addWidget(signal_list_combo)
        layout.addWidget(add_signal_button)

        # Restore saved signals
        for signal in self.saved_signals:
            self.add_signal_row(signal['type'], signal['params'])

        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll_layout.addLayout(self.form_layout)
        layout.addWidget(scroll)

        # 下一个和上一个按钮
        button_layout = QHBoxLayout()
        back_button = QPushButton('上一步')
        back_button.clicked.connect(self.back_window)
        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.save_and_next)
        button_layout.addStretch(1)
        button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_signal_row(self, signal_type, params=None):
        row_layout = QHBoxLayout()
        signal_label = QLabel(signal_type)
        row_layout.addWidget(signal_label)

        amplitude_input = QDoubleSpinBox()
        amplitude_input.setRange(0, 10)
        amplitude_input.setValue(params['amplitude'] if params else 1)
        row_layout.addWidget(QLabel("幅值:"))
        row_layout.addWidget(amplitude_input)

        # Add frequency input based on signal type
        if signal_type in ['正弦波', '方波', '三角波', '锯齿波']:
            frequency_input = QSpinBox()
            frequency_input.setRange(1, 1000)
            frequency_input.setValue(params['frequency'] if params else 10)
            row_layout.addWidget(QLabel("频率:"))
            row_layout.addWidget(frequency_input)

        # Add specific signal parameters (e.g., duty cycle for square wave)
        # ...

        self.form_layout.addLayout(row_layout)
        self.signal_entries.append((signal_type, {'amplitude': amplitude_input, 'frequency': frequency_input}))

    def save_and_next(self):
        # Save all current signal parameters
        saved_signals = []
        for entry in self.signal_entries:
            signal_type = entry[0]
            params = {
                'amplitude': entry[1]['amplitude'].value(),
                'frequency': entry[1]['frequency'].value() if 'frequency' in entry[1] else None,
                # Add other params here if needed
            }
            saved_signals.append({'type': signal_type, 'params': params})

        self.close()
        self.filter_window = FilterSelectionWindow(saved_signals=saved_signals)
        self.filter_window.show()

    def back_window(self):
        self.close()
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()


class FilterSelectionWindow(BaseWindow):
    def __init__(self, saved_signals):
        super().__init__('滤波器选择与参数设置')
        self.saved_signals = saved_signals
        self.saved_filter = None  # 初始没有选择滤波器

        # 创建布局
        layout = QVBoxLayout()
        self.label = QLabel("选择滤波器并设置参数：")
        layout.addWidget(self.label)

        # 添加滤波器选择部分
        self.filter_group = QGroupBox("选择滤波器")
        filter_layout = QVBoxLayout()

        # 滤波器类型选项（单选按钮）
        self.filter_buttons = {}
        filter_types = ['低通', '高通', '带通', '带阻', '巴特沃兹', '切比雪夫']
        self.selected_filter = None
        for f_type in filter_types:
            btn = QRadioButton(f_type)
            btn.toggled.connect(self.filter_selected)
            filter_layout.addWidget(btn)
            self.filter_buttons[f_type] = btn
        
        self.filter_group.setLayout(filter_layout)
        layout.addWidget(self.filter_group)

        # 滤波器参数设置部分
        self.param_group = QGroupBox("滤波器参数设置")
        param_layout = QVBoxLayout()

        self.order_label = QLabel("阶数：")
        self.order_input = QSpinBox()
        self.order_input.setRange(1, 10)
        param_layout.addWidget(self.order_label)
        param_layout.addWidget(self.order_input)

        self.cutoff_label = QLabel("截止频率：")
        self.cutoff_input = QDoubleSpinBox()
        self.cutoff_input.setRange(0.01, 1000.0)
        self.cutoff_input.setSingleStep(0.1)
        param_layout.addWidget(self.cutoff_label)
        param_layout.addWidget(self.cutoff_input)

        self.ripple_label = QLabel("纹波(切比雪夫)：")
        self.ripple_input = QDoubleSpinBox()
        self.ripple_input.setRange(0.01, 5.0)
        self.ripple_input.setSingleStep(0.1)
        param_layout.addWidget(self.ripple_label)
        param_layout.addWidget(self.ripple_input)
        self.ripple_label.hide()
        self.ripple_input.hide()

        self.param_group.setLayout(param_layout)
        layout.addWidget(self.param_group)

        # 上一步和下一步按钮
        button_layout = QHBoxLayout()
        back_button = QPushButton('上一步')
        back_button.clicked.connect(self.back_window)
        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        button_layout.addStretch(1)
        button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def filter_selected(self):
        # 获取选中的滤波器类型并显示相应的参数设置
        for f_type, btn in self.filter_buttons.items():
            if btn.isChecked():
                self.selected_filter = f_type
                if f_type == '切比雪夫':
                    self.ripple_label.show()
                    self.ripple_input.show()
                else:
                    self.ripple_label.hide()
                    self.ripple_input.hide()

    def next_window(self):
        # 保存滤波器的参数
        if not self.selected_filter:
            QMessageBox.warning(self, "警告", "请选择一个滤波器")
            return

        filter_params = {
            'order': self.order_input.value(),
            'cutoff': self.cutoff_input.value(),
            'ripple': self.ripple_input.value() if self.selected_filter == '切比雪夫' else None,
            'type': self.selected_filter.lower()
        }
        self.saved_filter = {'type': self.selected_filter, 'params': filter_params}

        # 打开结果展示窗口
        self.close()
        self.result_window = ResultWindow(self.saved_signals, self.saved_filter)
        self.result_window.show()

    def back_window(self):
        self.close()
        self.signal_window = SignalSelectionWindow(saved_signals=self.saved_signals)
        self.signal_window.show()


class ResultWindow(BaseWindow):
    def __init__(self, saved_signals, saved_filter):
        super().__init__('结果输出')
        self.saved_signals = saved_signals
        self.saved_filter = saved_filter

        # 创建布局
        layout = QVBoxLayout()
        self.label = QLabel("显示滤波前后的信号和滤波器特性：")
        layout.addWidget(self.label)

        # 创建matplotlib画布
        self.fig = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # 下一个和上一个按钮
        button_layout = QHBoxLayout()
        back_button = QPushButton('上一步')
        back_button.clicked.connect(self.back_window)
        finish_button = QPushButton('完成')
        finish_button.clicked.connect(self.finish_application)
        button_layout.addStretch(1)
        button_layout.addWidget(back_button)
        button_layout.addWidget(finish_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # 绘制信号
        self.plot_results()

    def plot_results(self):
        sample_rate = 1000  # 假设采样率为 1000 Hz
        input_signal = self.generate_input_signal()
        filter_response = apply_filter(input_signal, self.saved_filter['type'], self.saved_filter['params'], sample_rate)
        output_signal = generate_convolved_output(input_signal, filter_response)

        self.fig.clear()
        ax = self.fig.subplots(3, 3)

        t = np.linspace(0, 1, len(input_signal))  # 时间轴
        input_fft = np.fft.fft(input_signal)
        filter_fft = np.fft.fft(filter_response)
        output_fft = np.fft.fft(output_signal)
        freqs = np.fft.fftfreq(len(input_signal), 1 / sample_rate)

        # 时域图
        ax[0, 0].plot(t, input_signal)
        ax[0, 0].set_title('输入信号时域图')
        ax[1, 0].plot(t, filter_response)
        ax[1, 0].set_title('滤波器时域响应')
        ax[2, 0].plot(t, output_signal)
        ax[2, 0].set_title('输出信号时域图')

        # 幅频响应
        ax[0, 1].plot(freqs, np.abs(input_fft))
        ax[0, 1].set_title('输入信号幅频响应')
        ax[1, 1].plot(freqs, np.abs(filter_fft))
        ax[1, 1].set_title('滤波器幅频响应')
        ax[2, 1].plot(freqs, np.abs(output_fft))
        ax[2, 1].set_title('输出信号幅频响应')

        # 相频响应
        ax[0, 2].plot(freqs, np.angle(input_fft))
        ax[0, 2].set_title('输入信号相频响应')
        ax[1, 2].plot(freqs, np.angle(filter_fft))
        ax[1, 2].set_title('滤波器相频响应')
        ax[2, 2].plot(freqs, np.angle(output_fft))
        ax[2, 2].set_title('输出信号相频响应')

        self.canvas.draw()

    def generate_input_signal(self):
        # 根据用户选择的信号生成叠加的输入信号序列
        t = np.linspace(0, 1, 1000)  # 假设1秒的信号长度
        signal_sum = np.zeros_like(t)
        
        for signal in self.saved_signals:
            params = signal['params']
            if signal['type'] == '正弦波':
                signal_sum += params['amplitude'] * np.sin(2 * np.pi * params['frequency'] * t)
            elif signal['type'] == '方波':
                from scipy import signal as sp_signal
                signal_sum += params['amplitude'] * sp_signal.square(2 * np.pi * params['frequency'] * t)
            # 添加其他信号类型
        return signal_sum

    def back_window(self):
        self.close()
        self.filter_window = FilterSelectionWindow(saved_signals=self.saved_signals)
        self.filter_window.show()

    def finish_application(self):
        self.close()
        QApplication.quit()



    def finish(self):
        self.close()
