from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout, QScrollArea, QWidget, QSpinBox, QDoubleSpinBox, QMessageBox
from gui_base import BaseWindow
from gui_filter_selection import FilterSelectionWindow
import numpy as np

class SignalSelectionWindow(BaseWindow):
    def __init__(self, saved_signals=None):
        super().__init__('信号选择')
        self.saved_signals = saved_signals if saved_signals else []
        self.signal_entries = [] # 存储用户输入的信号信息
        layout = QVBoxLayout() # 用于组织界面布局

        self.form_layout = QVBoxLayout()

        # 创建信号类型的下拉选择框
        signal_list_combo = QComboBox()
        signal_list_combo.addItems(['正弦波', '方波', '三角波', '锯齿波', '白噪声', '高斯噪声', '脉冲噪声'])
        # 创建“添加信号”按钮
        add_signal_button = QPushButton('添加信号')
        add_signal_button.clicked.connect(lambda: self.add_signal_row(signal_list_combo.currentText()))
        layout.addWidget(signal_list_combo)
        layout.addWidget(add_signal_button)

        # 如果有已保存的信号 则为每个信号调用 add_signal_row 方法进行显示
        for signal in self.saved_signals:
            self.add_signal_row(signal['type'], signal['params'])

        # 创建一个滚动区域 scroll
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll_layout.addLayout(self.form_layout)
        layout.addWidget(scroll)

        # 创建“上一步”，“下一步”方法
        button_layout = QHBoxLayout()
        # 有 bug 先去掉
        # back_button = QPushButton('上一步')
        # back_button.clicked.connect(self.back_window)
        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.save_and_next)
        
        # 将按钮添加到布局中并设置窗口的总体布局
        button_layout.addStretch(1)
        # button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    # 为指定的信号类型添加输入行
    def add_signal_row(self, signal_type, params=None):
        # 创建一个水平布局
        row_layout = QHBoxLayout()
        signal_label = QLabel(signal_type)
        row_layout.addWidget(signal_label)

        # 幅值输入框
        amplitude_input = QDoubleSpinBox()
        amplitude_input.setRange(0, 1000)
        amplitude_input.setValue(params.get('amplitude', 1) if params else 1)
        row_layout.addWidget(QLabel("幅值:"))
        row_layout.addWidget(amplitude_input)

        # 根据信号类型设置额外的参数输入
        if signal_type in ['正弦波', '方波', '三角波', '锯齿波']:
            # 周期输入
            period_input = QDoubleSpinBox()
            period_input.setRange(0.01, 1000)
            period_input.setValue(params.get('period', 1) if params else 1)
            row_layout.addWidget(QLabel("周期:"))
            row_layout.addWidget(period_input)
            
            if signal_type == '正弦波':
                # 相位输入
                phase_input = QDoubleSpinBox()
                phase_input.setRange(-3.14, 3.14)
                phase_input.setValue(params.get('phase', 0) if params else 0)
                row_layout.addWidget(QLabel("相位:"))
                row_layout.addWidget(phase_input)
            elif signal_type == '方波':
                # 占空比输入
                duty_cycle_input = QDoubleSpinBox()
                duty_cycle_input.setRange(0, 1)
                duty_cycle_input.setValue(params.get('duty', 0.5) if params else 0.5)
                row_layout.addWidget(QLabel("占空比:"))
                row_layout.addWidget(duty_cycle_input)
        elif signal_type == '白噪声':
            # 白噪声参数
            mean_input = QDoubleSpinBox()
            mean_input.setRange(-10, 10)
            mean_input.setValue(params.get('mean', 0) if params else 0)
            row_layout.addWidget(QLabel("均值:"))
            row_layout.addWidget(mean_input)

            stddev_input = QDoubleSpinBox()
            stddev_input.setRange(0.01, 5.0)
            stddev_input.setValue(params.get('stddev', 1) if params else 1)
            row_layout.addWidget(QLabel("标准差:"))
            row_layout.addWidget(stddev_input)
        elif signal_type == '高斯噪声':
            # 高斯噪声参数同样处理
            mean_input = QDoubleSpinBox()
            mean_input.setRange(-10, 10)
            mean_input.setValue(params.get('mean', 0) if params else 0)
            row_layout.addWidget(QLabel("均值:"))
            row_layout.addWidget(mean_input)

            stddev_input = QDoubleSpinBox()
            stddev_input.setRange(0.01, 5.0)
            stddev_input.setValue(params.get('stddev', 1) if params else 1)
            row_layout.addWidget(QLabel("标准差:"))
            row_layout.addWidget(stddev_input)
        elif signal_type == '脉冲噪声':
            # 脉冲噪声的参数
            rate_input = QDoubleSpinBox()
            rate_input.setRange(0.01, 5.0)
            rate_input.setValue(params.get('rate', 1) if params else 1)
            row_layout.addWidget(QLabel("脉冲率:"))
            row_layout.addWidget(rate_input)
        elif signal_type == '直流':
            # 直流信号的直流量大小
            dc_value_input = QDoubleSpinBox()
            dc_value_input.setRange(-10, 10)
            dc_value_input.setValue(params.get('dc_value', 0) if params else 0)
            row_layout.addWidget(QLabel("直流量:"))
            row_layout.addWidget(dc_value_input)

        # 创建删除按钮
        delete_button = QPushButton("删除")
        delete_button.clicked.connect(lambda: self.remove_signal_row(row_layout))
        row_layout.addWidget(delete_button)

        # 将新创建的输入行添加到 form_layout
        self.form_layout.addLayout(row_layout)
        
        # 将输入控件的引用保存到 signal_entries 列表中，以便后续读取数据
        signal_params = {
            'amplitude': amplitude_input,
            'period': period_input if signal_type in ['正弦波', '方波', '三角波', '锯齿波'] else None,
            'phase': phase_input if signal_type == '正弦波' else None,
            'duty': duty_cycle_input if signal_type == '方波' else None,
            'mean': mean_input if signal_type in ['白噪声', '高斯噪声'] else None,
            'stddev': stddev_input if signal_type in ['白噪声', '高斯噪声'] else None,
            'rate': rate_input if signal_type == '脉冲噪声' else None,
            'dc_value': dc_value_input if signal_type == '直流' else None,
        }
        self.signal_entries.append({'type': signal_type, 'params': signal_params, 'layout': row_layout})



        
    # 遍历 signal_entries 中的每个信号
    # 把这次新增的加到save_signals中
    def save_and_next(self):
        saved_signals = []
        for entry in self.signal_entries:
            signal_type = entry['type']
            params = {
                'amplitude': entry['params']['amplitude'].value(),
                'period': entry['params']['period'].value() if entry['params']['period'] else None,
                'phase': entry['params']['phase'].value() if entry['params']['phase'] else None,
                'duty': entry['params']['duty'].value() if entry['params']['duty'] else None,
                'mean': entry['params']['mean'].value() if entry['params']['mean'] else None,
                'stddev': entry['params']['stddev'].value() if entry['params']['stddev'] else None,
                'rate': entry['params']['rate'].value() if entry['params']['rate'] else None,
                'dc_value': entry['params']['dc_value'].value() if entry['params']['dc_value'] else None,
            }
            saved_signals.append({'type': signal_type, 'params': params})

        if not saved_signals:
            QMessageBox.warning(self, "警告", "请选择一个信号")
            return

        self.close()
        self.filter_window = FilterSelectionWindow(saved_signals=saved_signals)
        self.filter_window.show()

    
    
    def remove_signal_row(self, row_layout):
        # 找到与该行对应的信号条目并删除
        for i, entry in enumerate(self.signal_entries):
            if entry['layout'] == row_layout:
                self.signal_entries.pop(i)
                break
        # 删除布局中的控件
        for i in reversed(range(row_layout.count())): 
            widget = row_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # 删除该行布局
        row_layout.deleteLater()


    # def back_window(self):
    #     self.close()
    #     self.welcome_window = WelcomeWindow()
    #     self.welcome_window.show()

    # 移除指定行的信号条目
    def remove_signal_row(self, row_layout):
        for i, entry in enumerate(self.signal_entries):
            if entry['layout'] == row_layout:
                # 从signal_entries中删除该信号
                self.signal_entries.pop(i)
                break

        # 删除布局中的控件
        while row_layout.count():
            widget = row_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()
        
        # 删除该行布局
        row_layout.deleteLater()