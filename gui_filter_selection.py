from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QGroupBox, QRadioButton, QSpinBox, QDoubleSpinBox, QMessageBox
from gui_base import BaseWindow
from gui_result import ResultWindow

class FilterSelectionWindow(BaseWindow):
    def __init__(self, saved_signals):
        super().__init__('滤波器选择与参数设置')
        self.saved_signals = saved_signals  # 存储从信号选择窗口传递过来的信号数据
        self.saved_filter = None

        # 创建一个垂直布局
        layout = QVBoxLayout()
        self.label = QLabel("选择滤波器并设置参数：")
        layout.addWidget(self.label)

        # 不同滤波器类型选择
        self.filter_group = QGroupBox("选择滤波器")
        filter_layout = QVBoxLayout()

        # 初始化一个字典 filter_buttons 存储各个滤波器按钮
        self.filter_buttons = {}
        filter_types = [
            '巴特沃兹低通', '巴特沃兹高通', '巴特沃兹带通', '巴特沃兹带阻',
            '切比雪夫1型低通', '切比雪夫1型高通', '切比雪夫1型带通', '切比雪夫1型带阻',
            '切比雪夫2型低通', '切比雪夫2型高通', '切比雪夫2型带通', '切比雪夫2型带阻'
        ]
        self.selected_filter = None

        for f_type in filter_types:
            btn = QRadioButton(f_type)
            btn.toggled.connect(self.filter_selected)
            filter_layout.addWidget(btn)
            self.filter_buttons[f_type] = btn

        # 将 filter_layout 赋给 filter_group，并添加到主布局中
        self.filter_group.setLayout(filter_layout)
        layout.addWidget(self.filter_group)

        # 创建滤波器参数输入组
        self.param_group = QGroupBox("滤波器参数设置")
        param_layout = QHBoxLayout()

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

        self.low_cutoff_label = QLabel("下截止频率：")
        self.low_cutoff_input = QDoubleSpinBox()
        self.low_cutoff_input.setRange(0.01, 1000.0)
        self.low_cutoff_input.setSingleStep(0.1)
        self.low_cutoff_label.hide()
        self.low_cutoff_input.hide()
        param_layout.addWidget(self.low_cutoff_label)
        param_layout.addWidget(self.low_cutoff_input)

        self.high_cutoff_label = QLabel("上截止频率：")
        self.high_cutoff_input = QDoubleSpinBox()
        self.high_cutoff_input.setRange(0.01, 1000.0)
        self.high_cutoff_input.setSingleStep(0.1)
        self.high_cutoff_label.hide()
        self.high_cutoff_input.hide()
        param_layout.addWidget(self.high_cutoff_label)
        param_layout.addWidget(self.high_cutoff_input)

        self.ripple_label = QLabel("纹波(切比雪夫)：")
        self.ripple_input = QDoubleSpinBox()
        self.ripple_input.setRange(0.01, 5.0)
        self.ripple_input.setSingleStep(0.1)
        self.ripple_label.hide()
        self.ripple_input.hide()
        param_layout.addWidget(self.ripple_label)
        param_layout.addWidget(self.ripple_input)

        self.param_group.setLayout(param_layout)
        layout.addWidget(self.param_group)

        # 添加“上一步”和“下一步”按钮
        button_layout = QHBoxLayout()
        # 因为分了文件后会出 bug 所以先去掉
        # back_button = QPushButton('上一步')
        # back_button.clicked.connect(self.back_window)
        next_button = QPushButton('下一步')
        next_button.clicked.connect(self.next_window)
        button_layout.addStretch(1)
        # button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def filter_selected(self):
        """根据选择的滤波器类型显示相应的参数输入"""
        for f_type, btn in self.filter_buttons.items():
            if btn.isChecked():
                self.selected_filter = f_type

                # 如果是带通或带阻滤波器，显示上截止频率和下截止频率输入框
                if '带通' in f_type or '带阻' in f_type:
                    self.low_cutoff_label.show()
                    self.low_cutoff_input.show()
                    self.high_cutoff_label.show()
                    self.high_cutoff_input.show()
                    self.cutoff_label.hide()
                    self.cutoff_input.hide()
                else:
                    self.low_cutoff_label.hide()
                    self.low_cutoff_input.hide()
                    self.high_cutoff_label.hide()
                    self.high_cutoff_input.hide()
                    self.cutoff_label.show()
                    self.cutoff_input.show()

                # 如果是切比雪夫类型的滤波器，显示纹波输入框
                if '切比雪夫' in f_type:
                    self.ripple_label.show()
                    self.ripple_input.show()
                else:
                    self.ripple_label.hide()
                    self.ripple_input.hide()

    def next_window(self):
        """收集用户选择的滤波器参数并打开结果展示窗口"""
        if not self.selected_filter:
            QMessageBox.warning(self, "警告", "请选择一个滤波器")
            return

        filter_params = {
            'order': self.order_input.value(),
            'ripple': self.ripple_input.value() if '切比雪夫' in self.selected_filter else None,
            'type': self.selected_filter.lower()
        }

        # 对于带通或带阻滤波器，使用上、下截止频率
        if '带通' in self.selected_filter or '带阻' in self.selected_filter:
            filter_params['low_cut'] = self.low_cutoff_input.value()
            filter_params['high_cut'] = self.high_cutoff_input.value()
        else:
            filter_params['cutoff'] = self.cutoff_input.value()

        self.saved_filter = {'type': self.selected_filter, 'params': filter_params}

        self.close()
        self.result_window = ResultWindow(self.saved_signals, self.saved_filter)
        self.result_window.show()

    # def back_window(self):
    #     """返回到信号选择窗口"""
    #     self.close()
    #     self.signal_window = SignalSelectionWindow(saved_signals=self.saved_signals)
    #     self.signal_window.show()
